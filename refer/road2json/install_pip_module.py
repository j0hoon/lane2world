import importlib

def install_pip_module(module_name = ""):
    '''
    python 모듈을 설치하는 함수 입니다. \n\n
    새로운 환경에서 python 코드를 실행하더라도 환경설정이 자동으로 되도록 하기 위해 사용합니다.  
    일반적으로 코드 실행 시 import 되는 모듈을 선언하기 전에 실행하는것이 좋습니다.  
    
    다른 코드에서 실행하고 싶은 경우   
    "from install_pip_module import install_pip_module" 을 선언한 후 사용하시기 바랍니다.   
    
    [input]/[output]  
    [input] : module_name(str)  
    [output] : 입력에 있는 모듈이 설치되어 있지 않으면 설치하고, 설치되어 있으면 이미 설치되어 있다는 메시지를 출력합니다.  
    
    [example]  
    [example 1] : install_pip_module("numpy")  
    [output 1] : numpy 모듈이 이미 설치되어 있습니다.  
    
    [example 2] : install_pip_module("pymongo")   
    [output 2] : pymongo 모듈이 설치되어 있지 않습니다. 설치를 진행합니다...    
    
    [주의사항]   
    주의할 사항으로는 입력하는 모듈의 이름은 pip에서 사용하는 이름과 동일해야 합니다.    
    또한 모듈 이름만 입력해야 합니다.    
    
    예를 들어, pymongo를 설치하고 싶으면 pymongo를 입력해야 합니다.     
    
    pip 모듈의 경우 실제로 설치되는 모듈의 이름과 다르게 사용되는 경우가 있습니다.    
    이런 부분을 주의하여 설치하시기 바랍니다.    
    
    [version]    
    v0.0.1 2023.05.10 JYH    
    코드 생성 및 주석 추가    
    '''
    try:
        importlib.import_module(module_name)
        print(f"{module_name} 모듈이 이미 설치되어 있습니다.")
    except ImportError:
        print(f"{module_name} 모듈이 설치되어 있지 않습니다. 설치를 진행합니다...")
        try:
            import pip
            pip.main(['install', module_name])
            print(f"{module_name} 모듈이 설치되었습니다.")
        except Exception as e:
            print(f"{module_name} 모듈 설치 중 오류가 발생했습니다:", str(e))

if __name__ == "__main__":

    print(install_pip_module.__doc__)
    # # 설치할 모듈 리스트
    # modules = ["numpy", "pandas", "matplotlib", "seaborn","pymongo","os","matplotlib","datetime","bson","dataframe-image"]

    # # 모듈 설치
    # for module in modules:
    #     install_pip_module(module)
