from pathlib import Path
class StorageService:
    def upload_bytes(self, content: bytes, key: str) -> str:
        upload_dir = Path('/tmp/ai_document_assistant_uploads')
        upload_dir.mkdir(parents=True, exist_ok=True)
        path = upload_dir / key.replace('/', '_')
        path.write_bytes(content)
        return str(path)
    def resolve_local_path(self, storage_key: str) -> str:
        return storage_key
