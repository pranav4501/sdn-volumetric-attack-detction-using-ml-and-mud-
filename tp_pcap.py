import pandas as pd
import pickle



def main():
	df= pd.read_csv ('6-6-18.csv')
	dp=pickle.load(open('6-6-18pickle.pkl','rb'))
	src= dp['Source'].tolist()
	dest= dp['Destination'].tolist()
	N,T,S,D,P,L,I=[],[],[],[],[],[],[]
	c=0
	for i in range(0,len(src)):
		li=[]
		if(df['Source'][i]=='192.168.1.227' or df['Destination'][i]=='192.168.1.227'):
			n=df['No.'][i]
			t=df['Time'][i]
			s=df['Source'][i]
			d=df['Destination'][i]
			p=df['Protocol'][i]
			l=df['Length'][i]
			inf=df['Info'][i]
			#li=[n,t,s,d,p,l,i]
			#print(li)
			'''li.append(n)
			li.append(t)
			li.append(s)
			li.append(d)
			li.append(p)
			li.append(l)
			li.append(i)'''
			#dk = pd.DataFrame(li,columns=['No.','Time','Source','Destination','Protocol','length','Info'])
			#dk.to_csv('/home/p4/p4-tools/p4-learning/exercises/Demo2/tplink.csv',index='False')
			N.append(n)
			T.append(t)
			S.append(s)
			D.append(d)
			P.append(p)
			L.append(l)
			I.append(inf)
			c=c+1
			print(c)


	dictionary = {'No.':N,'Time':T,'Source':S,'Destination':D,'Protocol':P,'length':L,'Info':I}
	dk = pd.DataFrame(dictionary)
	print(dk)
	dk.to_csv("6-6-18tplink.csv")
			


if __name__ == '__main__':
	main()