"""Decodifica rótulos de conversão do Google Ads.

O rótulo é base64url de: 3 bytes de prefixo + protobuf com
campo 1 = código do tipo de conversão (ctId) e campo 2 = ID da conta (AW-...).
Comparar o campo 2 com o ID configurado na tag revela tags que nunca registram:
o rótulo foi copiado de uma conta e o ID da tag é de outra.

Uso:
    python3 decode_label.py <rotulo> [id_configurado_na_tag]
    python3 decode_label.py XwY3CNKF2MwEEKzL2ucp 11223344556   # exemplo fictício
"""
import base64
import sys

PREFIXO = bytes([0x5F, 0x06, 0x37])


def _read_varint(buf: bytes, i: int) -> tuple[int, int]:
    value, shift = 0, 0
    while True:
        byte = buf[i]
        i += 1
        value |= (byte & 0x7F) << shift
        shift += 7
        if byte < 0x80:
            return value, i


def _varint(n: int) -> bytes:
    out = bytearray()
    while True:
        byte, n = n & 0x7F, n >> 7
        out.append(byte | 0x80 if n else byte)
        if not n:
            return bytes(out)


def decode(label: str) -> dict:
    raw = base64.urlsafe_b64decode(label + "=" * (-len(label) % 4))
    fields, i = {}, 3
    while i < len(raw):
        key = raw[i]
        value, i = _read_varint(raw, i + 1)
        fields[key >> 3] = value
    return {"ctId": fields.get(1), "aw_id": fields.get(2)}


def encode(ct_id: int, aw_id: int) -> str:
    """Inverso de decode; usado nos testes para gerar rótulos fictícios."""
    raw = PREFIXO + b"\x08" + _varint(ct_id) + b"\x10" + _varint(aw_id)
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    result = decode(sys.argv[1])
    print(f"ctId={result['ctId']}  conta_do_rotulo=AW-{result['aw_id']}")
    if len(sys.argv) > 2:
        configured = int(sys.argv[2].replace("AW-", ""))
        ok = configured == result["aw_id"]
        print("OK: ID da tag bate com o rótulo" if ok else f"DIVERGE: tag envia para AW-{configured}")


if __name__ == "__main__":
    main()
