import time
from module import DimensionalFormula, MultiprocessingDimensionalFormula


if __name__ == "__main__":
    print("---N차원 수식 객체를 생성합니다.---")
    equation = input(
        """방정식 양자를 입력해주세요 - 객체를 구성하는 최소단위 입니다. 예시) '3n/7+n**2'
        _:"""
    )
    unit_length = int(
        input(
            """단위 길이를 입력해주세요 - 1차원 직선상에 놓이는 방정식 양자의 갯수입니다.
        (단위 길이가 없으면 하나의 객체가 아닌 무한한 공간이 되기 때문에 연산이 불가능합니다)
        _:"""
        )
    )
    coupler = input(
        """방정식 양자들끼리 연결시키는 연산자를 입력해주세요.
        [ + , - , / , * , ** , // , % , ... ] 모두 사용 가능합니다.
        _:"""
    )
    dimension = int(
        input(
            """객체의 차원을 입력해주세요.
        차원인자는 연산량에 엄청난 차이를 가져옵니다.
        _:"""
        )
    )
    n = float(
        input(
            f"""연산을 진행하기 위해서 입력한 방정식 "{equation}"의 미지수 n을 입력해주세요.
        _:"""
        )
    )
    ins_for_serial_operations = DimensionalFormula(equation, coupler, unit_length, dimension)
    ins_for_parallel_operations = MultiprocessingDimensionalFormula(
        equation, coupler, unit_length, dimension
    )

    if not input("\n\n\n직렬로 연산을 진행합니다 Yes:그냥 엔터키 , 취소:아무 문자 입력 후 엔터"):
        start_time = time.time()
        start = time.strftime("%X", time.localtime(start_time))
        print(f"시작 : {start}")
        serial_result = ins_for_serial_operations.convert(n)
        print(f"연산결과 : {serial_result:.4f}")
        finish_time = time.time()
        finish = time.strftime("%X", time.localtime(finish_time))
        serial_time_delta = finish_time - start_time
        print(f"끝 : {finish}\n걸린시간 : {serial_time_delta:.3f}")
    else:
        serial_time_delta = None

    if not input("\n\n병렬로 연산을 진행합니다 Yes:그냥 엔터키 , 취소:아무 문자 입력 후 엔터"):
        start_time = time.time()
        start = time.strftime("%X", time.localtime(start_time))
        print(f"시작 : {start}")
        parallel_result = ins_for_parallel_operations.multiprocessing_convert(n)
        print(f"연산결과 : {parallel_result:.4f}")
        finish_time = time.time()
        finish = time.strftime("%X", time.localtime(finish_time))
        parallel_time_delta = finish_time - start_time
        print(f"끝 : {finish}\n걸린시간 : {parallel_time_delta:.3f}")
    else:
        parallel_time_delta = None

    if parallel_time_delta and serial_time_delta:
        print(f"\n\n일반 직렬 연산 결과 : {serial_result:.4f} __ 병렬연산 결과 : {parallel_result:.4f}")
        print(
            f"""
        이 컴퓨터의 CPU코어수는 {ins_for_parallel_operations.cpu_count}개 입니다. 병렬 프로그레밍으로 최대 {ins_for_parallel_operations.cpu_count}배 빨라질 수 있음을 의미합니다.
        연산에 사용된 방정식 양자의 갯수는 총 {unit_length**dimension}개 입니다.
        
        병렬 연산 시에는 {unit_length**dimension}개의 방정식 양자를 {ins_for_parallel_operations.cpu_count}개의 CPU코어들에게 최대한 균등하게 할당합니다.
        메인 쓰레드가 각 CPU들에게서 연산 결과를 (거의 동시에)전달받은 뒤에
        그것들로 최종 결과를 연산하여 값을 반환합니다.

        CPU 멀티코어를 사용해서 연산했을때 {serial_time_delta/parallel_time_delta:.3f}배 더 빨랐습니다.
        """
        )
