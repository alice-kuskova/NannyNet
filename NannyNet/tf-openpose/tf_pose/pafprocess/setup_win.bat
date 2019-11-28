cd "C:\Users\Artem\source\repos\NannyNet\NannyNet\swigwin-4.0.1"
swig -python -c++ "C:\Users\Artem\source\repos\NannyNet\NannyNet\tf-openpose\tf_pose\pafprocess\pafprocess.i"
cd "C:\Users\Artem\source\repos\NannyNet\NannyNet\tf-openpose\tf_pose\pafprocess\"
set PATH=%PATH%;"C:\Users\Artem\source\repos\NannyNet\NannyNet\swigwin-4.0.1"
set PYTHON_LIB= "C:\Users\Artem\source\repos\NannyNet\NannyNet\swigwin-4.0.1"
set PYTHON_INCLUDE="C:\Users\Artem\source\repos\NannyNet\NannyNet\swigwin-4.0.1"
pythonw setup.py build_ext --inplace
pause