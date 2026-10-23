import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "auditoria-midia-chrome" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import decode_label  # noqa: E402


@pytest.mark.parametrize("ct_id,aw_id", [(1234567890, 11223344556), (7, 1), (2**40 + 3, 99999999999)])
def test_encode_decode_ida_e_volta(ct_id, aw_id):
    assert decode_label.decode(decode_label.encode(ct_id, aw_id)) == {"ctId": ct_id, "aw_id": aw_id}


def test_exemplo_da_documentacao():
    assert decode_label.decode("XwY3CNKF2MwEEKzL2ucp") == {"ctId": 1234567890, "aw_id": 11223344556}


@pytest.mark.parametrize("tag,esperado", [("11223344556", "OK"), ("AW-55555555555", "DIVERGE")])
def test_cli_compara_com_id_da_tag(tag, esperado):
    saida = subprocess.run(
        [sys.executable, str(SCRIPTS / "decode_label.py"), "XwY3CNKF2MwEEKzL2ucp", tag],
        capture_output=True, text=True, check=True,
    ).stdout
    assert esperado in saida
