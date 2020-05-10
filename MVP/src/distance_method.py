import scipy
import numpy as np

# TODO 需要確認所有 distance  和 cos (未正規化) 時是否一樣，還有公式適用於甚麼情況??
def distance(f, v):
    '''一般兩點距離'''
    assert len(f) == len(v), "len(feature) != len(vector)"

    return sum(v * f)/(np.sqrt(sum(np.square(v))) * np.sqrt(sum(np.square(f))))

def cosine_similarity_distance(f, v, norm=True):
    """餘弦相似度"""
    assert len(f) == len(v), "len(feature) != len(vector)"
    cos = np.dot(f, v)/(np.linalg.norm(f)*np.linalg.norm(v))

    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内

def euclidean_distance(f, v):
    '''歐幾里得距離'''
    assert len(f) == len(v), "len(feature) != len(vector)"

    return np.sqrt(sum(np.square(f - v)))

def pearsonr(f, v):
    '''person correlation coefficient（皮爾森相關性係數）'''
    assert len(f) == len(v), "len(feature) != len(vector)"

    return scipy.stats.pearsonr(f, v)[0]

def spearmanr(f, v):
    '''spearman correlation coefficient（斯皮爾曼相關性係數）'''
    assert len(f) == len(v), "len(feature) != len(vector)"
    
    return scipy.stats.spearmanr(f, v)[0]

def kendall(f, v):
    '''kendall correlation coefficient（肯德爾相關性係數)，適合類別的'''
    assert len(f) == len(v), "len(feature) != len(vector)"
    tau, p_value = scipy.stats.kendalltau(f, v)
    
    return tau