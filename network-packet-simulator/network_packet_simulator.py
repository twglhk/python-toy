import numpy as np

"""
lambda_: 패킷 도착률 (패킷/초)
processing_time: 각 패킷 처리 시간 (초)
total_time: 전체 시뮬레이션 시간 (초)
"""
def simulate_network_traffic(lambda_, processing_time, total_time=1, queue_limit=None):
    time = 0
    arrived_packets = 0
    processed_packets = 0
    
    # 패킷들의 도착 시간을 저장할 큐
    packet_queue = []
    
    # 패킷들이 도착한 중간 시간의 합이, 시간의 총합이 될 때까지 진행
    while time < total_time:
        # 패킷 도착
        # NumPy : 파이썬 수치 계산 라이브러리
        # exponential : 지수 분포는 한 사건에서 다음 사건까지의 대기 시간을 모델링 하는 데에
        #               자주 사용 됨. (ex : 네트워크 패킷 도착 간격 등)
        #               네트워크 패킷이 항상 일정하게 도착하는 것은 아니기 때문. (0.1초, 0.5초 등의 불규칙성을 모델링하기 위해 지수 분포 사용)
        # 1/lambda_ : 평균 도착 간격(초당 도착 패킷량을 역수를 취했기 때문). 
        #             크면 도착 간격은 짧아지고, 작으면 도착 간격은 길어짐.
        #             초당 도착하는 패킷의 양이 커지면 커질 수록 도착 간격이 짧아짐.
        # 결론적으로 이 부분은 패킷의 양에 따라 지수 분포값를을 랜덤하게 생성하여 중간 도착 시간에 저장.
        inter_arrival_time = np.random.exponential(1/lambda_)
        print(f"inter_arrival_time : {inter_arrival_time: .2f}")
        time += inter_arrival_time
        if time < total_time:
            arrived_packets += 1
            
            # 대기열 길이 제한 체크
            if queue_limit is None or len(packet_queue) < queue_limit:
                packet_queue.append(time)
            else:
                # 대기열이 가득 찼을 때의 패킷 드롭 로직
                pass
        
        # time = 패킷이 도착한 시간 + 패킷 처리 시간
        
        # 패킷 처리
        # if arrived_packets > processed_packets:
        #     time += processing_time
        #     processed_packets += 1
        if packet_queue and time - packet_queue[0] >= processing_time:
            processed_packets += 1
            packet_queue.pop(0)  # 첫 번째 패킷 처리
            
    # 리틀의 법칙 적용
    # 평균 대기 시간 (W) = 전체 시뮬레이션 시간 / 도착한 패킷 수
    W = total_time / arrived_packets if arrived_packets > 0 else 0
    L = lambda_ * W
    
    # return L, arrived_packets - processed_packets
    return L, len(packet_queue)
    
# Main    
# 패킷의 도착률(Lambda)보다 처리 시간이 빨라야 latency가 짧아짐.
print("Hello World")   
lambda_ = 15  # 초당 N개의 패킷 도착
processing_time = 0.8  # 패킷당 0.05초의 처리 시간
L, waiting_packets = simulate_network_traffic(lambda_, processing_time)
print(f"리틀의 법칙에 의한 대기 패킷 수: {L:.2f}")
print(f"실제 대기 패킷 수: {waiting_packets}")