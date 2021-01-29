import numpy as np
from flask import Flask,request,jsonify, render_template
import pickle
app=Flask(__name__,template_folder='template')
app._static_folder = 'static'
model1=pickle.load(open('model1.pkl','rb'))
model2=pickle.load(open('model2.pkl','rb'))
@app.route('/home')
def homepage():    
    return render_template('index.html')
@app.route('/advancedpage')
def advancedpage():    
    return render_template('index.html')
@app.route('/quick',methods=['POST'])
def quick():
	def bmi(height,weight):
		bmi=int(weight)/((int(height)/100)**2)
		return bmi
	int_features1 = [float(x) for x in request.form.values()]
		
	age=int_features1[1]
	cigs=int_features1[3]
	height=int_features1[8]
	weight=int_features1[9]
	hrv=int_features1[10]
	int_features1.pop(8)
	int_features1.pop(9)
	bmi=round(bmi(height,weight),2)
	int_features1.insert(8,bmi)
	
	if int(int_features1[0])==1.0:
		sex="Male"
	else:
		sex="Female"
	if int(int_features1[2])==1.0:
		smoking="Yes"
	else:
		smoking="No"
	if int(int_features1[4])==1.0:
		stroke="Yes"
	else:
		stroke="No"

	if int(int_features1[5])==1.0:
		hyp="Yes"
	else:
		hyp="No"
	if int(int_features1[7])==1.0:
		dia="Yes"
	else:
		dia="No"
	if int(int_features1[6])==1.0:
		bpmeds="Yes"
	else:
		bpmeds="No"
	

	final_feature1=[np.array(int_features1)]
	prediction1= model1.predict(final_feature1)
	result=prediction1[0]
	
	if result==0:
		result="No need to worry"
	else:
		result="You are detected with heart problems. You need to consult a doctor immediately"
	return render_template('quick_report.html',prediction_text1= result,gender=sex,age=age,smoking=smoking,cigs=cigs,stroke=stroke,hyp=hyp,dia=dia,bpmeds=bpmeds,bmi=bmi,hrv=hrv)
@app.route('/quickpage')
def quickpage():    
    return render_template('index1.html')
@app.route('/')
def home():    
    return render_template('Home.html')

@app.route('/advanced',methods=['POST'])
def advanced():
	int_features2 = [int(x) for x in request.form.values()]
	final2_feature=[np.array(int_features2)]
	prediction2= model2.predict(final2_feature)
	result=prediction2[0]

	age=int_features2[0]
	trestbps=int_features2[3]
	chol=int_features2[4]
	oldspeak=int_features2[7]
	thalach=int_features2[7]
	ca=int_features2[10]

	if int(int_features2[1])==1:
		sex="Male"
	else:
		sex="Female"
	
	if int(int_features2[2])==1:
		cp="Typical angina"
	elif int(int_features2[2])==2:
		cp="Atypical angina"
	elif int(int_features2[2])==3:
		cp="Non-angina pain"
	else:
		cp="Asymtomatic"
	
	
	if int(int_features2[5])==1:
		fbs="Yes"
	else:
		fbs="No"

	if int(int_features2[6])==1:
		restecg="ST-T wave abnormality"
	elif int(int_features2[6])==2:
		restecg="showing probable or definite left ventricular hypertrophy by Estes"
	else:
		restecg="Normal"

	if int(int_features2[8])==1:
		exang="Yes"
	else:
		exang="No"
		
	if int(int_features2[9])==1:
		slope="upsloping"
	elif int(int_features2[9])==2:
		slope="flat"
	else:
		slope="downsloping"
	
	if int(int_features2[11])==3:
		thal="Normal"
	elif int(int_features2[11])==6:
		thal="Fixed defect"
	else:
		thal=" reversable defect"

	if result==0:
		result="No need to worry"
	else:
		result="You are detected with heart problems. You need to consult a doctor immediately"
	return render_template('advance_report.html',prediction_text2= result,age=age,sex=sex,cp=cp,trestbps=trestbps,chol=chol,fbs=fbs,restecg=restecg,oldpeak=oldspeak,exang=exang,slope=slope,ca=ca,thal=thal)


if __name__=="__main__":
    app.run(debug=True)