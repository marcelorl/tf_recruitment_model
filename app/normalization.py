
# Imports
import joblib

# Carrega os arquivos do modelo


def normalization_(data):
    STANDARD_SCALER = joblib.load('std_scaler.pkl')
    QT_SCALER = joblib.load('qt_scaler.pkl')
    transformed = STANDARD_SCALER.transform(QT_SCALER.transform(data))
    return transformed
