## Thư viện API khuôn mặt

### Cài đặt
```
pip install wheel

pip install .
python setup.py sdist
python setup.py bdist_wheel
```

### Upload pip
```
twine upload dist/*

```

## GUIDE 

### ```pip install vlute_faces_services```

```angular2html
from vlute_faces_services import qllb

p = qllb("0889224db5e14133b379b74db0e21451")

# Lấy ds phòng trên hệ thống
print(p.ds_phong())

# mssv là SV cần điểm danh; phòng là id phòng lấy từ p.ds_phong()
print(p.diem_danh(mssv=5, phong=56))
```