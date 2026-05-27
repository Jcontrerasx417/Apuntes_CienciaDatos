import argparse
import tarfile
import zipfile
from pathlib import Path


def extract_tar(archive_path: Path, dest_dir: Path) -> None:
    with tarfile.open(archive_path, "r:*") as tar:
        tar.extractall(path=dest_dir)


def extract_zip(archive_path: Path, dest_dir: Path) -> None:
    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(dest_dir)


def find_archives(root: Path):
    archive_suffixes = {".tar", ".tar.gz", ".tgz", ".zip", ".tar.bz2", ".tbz2"}
    for path in root.rglob("*"):
        if path.is_file():
            suffix = path.suffix.lower()
            if suffix == ".tar" or suffix == ".zip":
                yield path
            elif suffix in {".gz", ".bz2"}:
                # detect double suffix for tar.gz, tar.bz2
                if path.name.lower().endswith(".tar.gz") or path.name.lower().endswith(".tar.bz2"):
                    yield path
            elif path.name.lower().endswith(".tgz") or path.name.lower().endswith(".tbz2"):
                yield path


def extract_all(root: Path, output_root: Path = None) -> None:
    output_root = output_root or root
    found_any = False

    for archive_path in find_archives(root):
        found_any = True
        relative_dir = archive_path.parent.relative_to(root)
        dest_dir = output_root / relative_dir / archive_path.stem
        dest_dir.mkdir(parents=True, exist_ok=True)

        print(f"Extrayendo {archive_path} -> {dest_dir}")
        try:
            if archive_path.suffix.lower() == ".zip":
                extract_zip(archive_path, dest_dir)
            else:
                extract_tar(archive_path, dest_dir)
        except (tarfile.TarError, zipfile.BadZipFile) as exc:
            print(f"Error al extraer {archive_path}: {exc}")

    if not found_any:
        print(f"No se encontraron archivos TAR/ZIP en {root}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Busca y descomprime archivos TAR / ZIP recursivamente.")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directorio raíz donde buscar archivos comprimidos (por defecto, el directorio actual).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Directorio destino para la extracción. Si no se especifica, extrae en el mismo árbol de directorios.",
    )
    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    output_path = Path(args.output).resolve() if args.output else None

    extract_all(root_path, output_path)
