import pickle

h = pd.read_csv('data/m1/0319-0417_subscribe_wl.csv', encoding='cp950')

s = pd.read_csv('data/m1/0410-0416_user_history.csv')


userid_ls = list(set(h.user_id.unique()) & set(s.user_id.unique()))

a = {'userid': userid_ls}

with open('data/user/userid.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('data/user/userid.pickle', 'rb') as handle:
    b = pickle.load(handle)