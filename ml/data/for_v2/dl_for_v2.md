설명 대상 파일: 03_deep_learning_pre3.ipynb
적용 시점: 0520

####  변경/적용 사항



## 코로나 컬럼


문제: 특수한 기간동안의 관객 수가 전체 예측에 영향을 미칠 것을 우려    
기준: 기간별 평균 관객 수

covid         294400.586842
post_covid    460403.418639
pre_covid     836858.838882

학습 적용: ['is_covid_period'] (이진 분류 컬럼 추가: covid=1 or 0)


## 피크 시즌 조정 컬럼


문제: 성수기 여부에 대한 직접적인 학습 영향 부족
기준: 12,1 (겨울 성수기)/ 7,8 (여름 성수기) & 그 외 기간의 관객 비교

                        count	mean	median	min	max
non_peak	            2661	544607	67313	260	13977409
summer_peak(7,8)	    613	    963585	100947	514	17583608
winter_peak(12,1)	    595	    892736	175320	259	16252575

학습 적용:[is_peak_season] (이진 분류 컬럼 추가: 12, 1, 7, 8 개봉 시 1 or 0)


## 검색 트렌드 조정 컬럼


문제: 다중공선성    
기준:상관관계

"trend_pre7_max" - "trend_pre7_avg" (0.92)  


trend_cols =  ["trend_pre7_avg", "trend_pre7_max", 
                "trend_growth_rate", "relative_search_share", "has_trend_data"]

학습 적용: [ "trend_pre7_max", "relative_search_share", "has_trend_data" ]

"trend_pre7_avg" 컬럼 삭제 (기준: log_audience 와의 상관관계)


## power balace 조정 컬럼

설명 내용과 중복되어 생략


## holidays 조정 컬럼


문제: 약한 상관관계
기준: 상관관계

대상: total_audience

is_holiday_release      0.015329
holiday_nearby_count    0.011592

변경점:
has_holiday_count (0,1) 이진 분류 컬럼 추가 
*그러나 이 역시 특별히 강한 상관관계가 나타나진 않았음 (오히려 감소)*

## 런타임
*단순 시도*
런타임 그룹화 시도 (ex: 70분 미만 short, 110분 미만 normal 등)

문제: 
목표: 모델 안정성 향상
효과가 아직 검증되지 않음

#####


### 학습 결과

*학습1: 단순 회귀*
    <target: log_audience>

    수치형: StandardScaler
    범주형: OneHotEncoder
    (layer = 4, input -> 128 -> 64 -> 32 -> 1, Dropout = yes)

MSE : 2.007274627685547
RMSE: 1.4167831971355205
MAE : 1.1288139820098877
R2  : 0.5725902915000916


*학습2: 단순 회귀 [원핫인코딩 대상 축소]*
    <target: log_audience>

    수치형: StandardScaler
    범주형: OneHotEncoder
    (layer = 4, input -> 128 -> 64 -> 32 -> 1, Dropout = yes)

MSE : 2.0990517139434814
RMSE: 1.4488104478997526
MAE : 1.147212028503418
R2  : 0.5530481338500977


*학습3: 단순 분류*
    <target: hit_class> class: 0, 1, 2, 3
    
    수치형: StandardScaler
    범주형: OneHotEncoder
    (layer = 4, input -> 128 -> 64 -> 32 -> 4, Dropout = yes)

Accuracy : 0.8320413436692506
Precision: 0.7983561131510948
Recall   : 0.8320413436692506
F1-score : 0.8132218276022344

Confusion Matrix
[[612  26   0  10]
 [ 49  22   0  10]
 [ 15   6   0   2]
 [  8   3   1  10]]

특이사항: 2클래스 적중 수 없음


*학습4: 가중치 분류*
    <target: hit_class> class: 0, 1, 2, 3
    
    수치형: StandardScaler
    범주형: OneHotEncoder
    (layer = 4, input -> 128 -> 64 -> 32 -> 4, Dropout = yes)

Accuracy : 0.7545219638242894
Precision: 0.837023096015193
Recall   : 0.7545219638242894
F1-score : 0.7860085325094726

Confusion Matrix
[[532  81   5  30]
 [ 19  38   5  19]
 [  3  10   1   9]
 [  3   4   2  13]]


 *학습5: 가중치 적용 회귀*
    <target: log_audience>

    수치형: StandardScaler
    범주형: OneHotEncoder
    (layer = 4, input -> 128 -> 64 -> 32 -> 1, Dropout = yes)

MSE : 2.948481798171997
RMSE: 1.7171143812140173
MAE : 1.3193292617797852
R2  : 0.41213756799697876

### 모든 모델은 동일한 레이어로 진행되었음