import pandas as pd
from io import BytesIO
import pytest
from src.services import extract_transactions_with_mobile_numbers


@pytest.fixture
def excel_file():
    data = {
        'Описание': ['+7 (123) 456-78-90 покупка', 'Нет моб. номера', '+7 123 456 78 90 оплата', None]
    }
    df = pd.DataFrame(data)

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return excel_file


@pytest.mark.parametrize("file_path, expected_result", [
    ('dummy_path.xlsx', None)
])
def test_extract_transactions_with_mobile_numbers(monkeypatch, file_path, expected_result, excel_file):
    def mock_read_excel(*args, **kwargs):
        return pd.read_excel(excel_file)

    monkeypatch.setattr(pd, 'read_excel', mock_read_excel)

    result = extract_transactions_with_mobile_numbers(file_path)
    assert result == expected_result
