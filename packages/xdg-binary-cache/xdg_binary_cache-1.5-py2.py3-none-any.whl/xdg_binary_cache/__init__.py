"""All the logic for xdg-binay-cache."""
import argparse
import contextlib
import fcntl
import logging
import os
from pathlib import Path
import shutil
import stat
import time
from typing import Iterable, Iterator, Optional
import subprocess
import urllib.request


LOGGER = logging.getLogger("xdg_binary_cache")

# The pattern that defines where to find the binary remotely.
REMOTE_URL = (
	"https://storage.googleapis.com/pre-commit-assets/"
	"{binary_name}/{version}/bin/{binary_name}"
)

class BinaryDownloader:
	"""Encapsulates the configuration information for downloading a binary."""
	def __init__(self, binary_name: str, version: str):
		"""Initialize the BinaryDownloader.

		Args:
			binary_name: The name of the binary managed by this downloader.
				This setting controls both the filename on the local host and
				the name seen by the user in help messages and logging output.
				Do not instantiate two BinaryDownloader with the same binary_name.
			version: The version string for the binary. This will be used to allow
				for multiple different versions of the same binary from different
				programs on the same host system.
		"""
		self._add_arguments_called = False
		self._handle_arguments_called = False

		self.binary_name = binary_name
		self.override_path: Optional[Path] = None
		self.override_url: Optional[str] = None
		self.version = version

	def add_arguments(self, parser: argparse.ArgumentParser) -> None:
		"""Add the commandline arguments this library cares about.

		Args:
			parser: The argparse.ArgumentParser instance to add arguments to.
		"""
		self._add_arguments_called = True
		parser.add_argument(
			f"--override-{self.binary_name}-path",
			type=Path,
			help=(f"Specify a path to a specific version of {self.binary_name} to use. "
				f"If this is provided then {self.binary_name} will not be downloaded but "
				"instead the local copy will be used directly."),
		)
		target_download_path = self.cached_binary_path()
		parser.add_argument(
			f"--override-{self.binary_name}-url",
			help=(f"Specify a URL to use when downloading {self.binary_name}. "
				f"If this is provided then if no copy of {self.binary_name} exists "
				f"at {target_download_path} then a copy will be downloaded from this "
				f"URL. If the URL provided contains a version of {self.binary_name} "
				f"other than {self.version}, it may be confusing since {self.version} "
				f"is part of the path '{target_download_path}'."),
		)

	def cached_binary_path(self) -> Path:
		"Get the path to the cached binary file on the local host."
		return self.cached_binary_root() / self.version / self.binary_name

	def cached_binary_root(self) -> Path:
		"Get the path to the root directory for the cached binary on the local host."
		cached_path = Path(os.environ.get("XDG_CACHE_HOME",
			os.path.join(os.environ["HOME"], ".cache")))
		return cached_path / self.binary_name

	def download_binary(self) -> Path:
		"""
		Download the remote binary to the local cache.

		Returns:
			The absolute path to the downloaded file.
		"""
		target_path = self.cached_binary_path()
		if target_path.exists():
			LOGGER.debug("Using previously downloaded %s at %s", self.binary_name, target_path)
			return target_path
		remote_url = self.remote_binary_url()
		LOGGER.info("Downloading %s version %s from %s", self.binary_name, self.version, remote_url)
		local_filename, _ = urllib.request.urlretrieve(remote_url)
		try:
			target_path.parent.mkdir(parents=True, exist_ok=True)
		except NotADirectoryError:
			# It could be that there exists an old cached binary at $XDG_CACHE_HOME/{binary_name}
			# from a previous version of this logic. We need to clear it out to make
			# room for this new logic.
			root = self.cached_binary_root()
			if root.exists():
				os.unlink(root)
			target_path.parent.mkdir(parents=True, exist_ok=True)
		# Fix file permissions on the source temporary file before moving. We
		# do this because as soon as we move to the final location we will release
		# the lock on the file and other processes may attempt to execute it.
		fix_file_permissions(Path(local_filename))
		LOGGER.debug("Getting IPCLock on %s", target_path)
		with lock_exclusive(target_path):
			shutil.move(local_filename, target_path)
		LOGGER.info("Downloaded %s from %s to %s and then moved to %s",
			self.binary_name, remote_url, local_filename, target_path)
		return target_path

	def handle_arguments(self, args: argparse.Namespace) -> None:
		"""
		Handle the arguments that were parsed from the argument parser.

		You must call this function before calling download_binary or execute_binary.

		Args:
			args: The args parsed from the argument parser.
		"""
		self._handle_arguments_called = True
		binary_name_no_hyphens = self.binary_name.replace("-", "_")
		override_path = getattr(args, f"override_{binary_name_no_hyphens}_path", None)
		self.override_path = override_path and Path(override_path)
		self.override_url = getattr(args, f"override_{binary_name_no_hyphens}_url", None)

	def skip_arguments(self) -> None:
		"""
		Skip handling arguments. This should only be used for tests.
		"""
		self._add_arguments_called = True
		self._handle_arguments_called = True

	def remote_binary_url(self) -> str:
		"""Get the remote URL to use when downloading the binary."""
		return self.override_url or REMOTE_URL.format(
			binary_name=self.binary_name,
			version=self.version,
		)

	def run_binary(self,
			args: Iterable[str],
			capture_output=True,
			check=True,
			encoding="UTF-8",
			**kwargs) -> subprocess.CompletedProcess:
		"""
		Execute the downloaded binary, wait for execution, return the result.
		Args:
			args: The arguments to pass to the binary.
			capture_output: See subprocess.run(capture_output).
			check: See subprocess.run(check).
			encoding: See subprocess.run(encoding).
			kwargs: arguments to pass to subprocess.run.
		Returns:
			The completed subprocess.run result.
		"""
		if not all((self._handle_arguments_called, self._add_arguments_called)):
			LOGGER.warning(
				"Looks like you haven't called BinaryDownloader.add_arguments() and "
				"BinaryDownloader.handle_arguments(). This means your users can't "
				"customize the binary downloader behavior.")
		if self.override_path:
			binary_path = self.override_path
		else:
			binary_path = self.download_binary()
		cmd = [str(binary_path)] + list(args)
		# Translate capture_output parameters for Python 3.6 compatibility
		if capture_output:
			if "stderr" in kwargs or "stdout" in kwargs:
				raise ValueError("Do not specify both capture_output and stdout/stderr")
			kwargs["stderr"] = subprocess.PIPE
			kwargs["stdout"] = subprocess.PIPE
		lock_shared(binary_path)
		try:
			return subprocess.run(
				cmd,
				check=check,
				encoding=encoding,
				**kwargs)
		except UnicodeDecodeError as ex:
			LOGGER.error("Failed to execute %s: %s", cmd, ex)
			raise

def fix_file_permissions(target_path: Path) -> None:
	"""Set the correct executable file permission flags.

	Args:
		target_path: The full path to the file to manipulate.
	"""
	try:
		os.chmod(target_path, (
			stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
			stat.S_IRGRP | stat.S_IXGRP |
			stat.S_IROTH | stat.S_IXOTH))
	except OSError as ex:
		LOGGER.warning("Failed to set chmod 755 for %s: %s", target_path, ex)

@contextlib.contextmanager
def lock_exclusive(path: Path) -> Iterator[None]:
	"""Exclusively lock the given file path with the OS for all processes.

	This is used to ensure that multiple instances of programs using this
	library cooperate and don't write to the file at the same time.
	"""
	LOGGER.debug("Getting exclusive lock on %s", path)
	if not path.exists():
		path.parent.mkdir(parents=True, exist_ok=True)
		path.touch()
	with open(path, "r") as target_file:
		fcntl.flock(target_file, fcntl.LOCK_EX)
		LOGGER.debug("Got exclusive lock on %s", path)
		yield
		fcntl.flock(target_file, fcntl.LOCK_UN)
		LOGGER.debug("Released exclusive lock on %s", path)

def lock_shared(path: Path) -> None:
	"""Get and release a shared lock on the given path.

	This function aquires AND IMMEDIATELY RELEASES a shared lock on a given
	file path. The purpose is just to wait on any exclusive locks, not to
	prevent additional exclusive locks from being aquired. This is because
	the nature of this program is that we need to subprocess.call the file
	we are locking which we can't do while a lock is held - at least, I don't
	think we can, and tests show I can't trivially.
	"""
	LOGGER.debug("Getting shared lock on %s", path)
	with open(path, "r") as target_file:
		fcntl.flock(target_file, fcntl.LOCK_SH)
		LOGGER.debug("Got shared lock on %s", path)
		fcntl.flock(target_file, fcntl.LOCK_UN)
		LOGGER.debug("Released shared lock on %s", path)
