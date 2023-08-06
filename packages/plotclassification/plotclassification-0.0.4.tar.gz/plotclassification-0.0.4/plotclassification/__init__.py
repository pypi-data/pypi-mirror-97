import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.metrics import precision_score,recall_score,f1_score
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score

class plot:
    def __init__(self,y,y_predict_proba,class_name):
        self.y=y
        self.y_predict_proba=y_predict_proba
        self.class_name=class_name
    def plot_roc(self):
        y_scores=self.y_predict_proba
        # One hot encode the labels in order to plot them
        y_onehot = pd.get_dummies(self.y,columns=self.class_name)
        y_onehot.columns=self.class_name
        # Create an empty figure, and iteratively add new lines
        # every time we compute a new class
        fig = go.Figure()
        fig.add_shape(type='line', line=dict(dash='dash'), x0=0, x1=1, y0=0, y1=1)
        for i in range(y_scores.shape[1]):
            y_true = y_onehot.iloc[:, i]
            y_score = y_scores[:, i]

            fpr, tpr, _ = roc_curve(y_true, y_score)
            auc_score = roc_auc_score(y_true, y_score)
            name = f"{y_onehot.columns[i]} (AUC={auc_score:.2f})"
            fig.add_trace(go.Scatter(x=fpr, y=tpr, name=name, mode='lines'))

        fig.update_layout(
            title='ROC Plot',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            yaxis=dict(scaleanchor="x", scaleratio=1),
            xaxis=dict(constrain='domain'),
            width=800, height=800,
            font=dict(size=18) ,title_x=0.5,
            margin=dict(l=10, r=10, t=100, b=10),
            legend=dict(yanchor='bottom',y=0.01,xanchor='right',x=0.65))
        return fig.show()

    def plot_precision_recall_curve(self):
        y_scores=self.y_predict_proba
        fig = go.Figure()
        fig.add_shape(type='line', line=dict(dash='dash'),x0=0, x1=1, y0=1, y1=0)
        y_onehot = pd.get_dummies(self.y,columns=self.class_name)
        y_onehot.columns=self.class_name
        for i in range(y_scores.shape[1]):
            y_true = y_onehot.iloc[:, i]
            y_score = y_scores[:, i]
            precision, recall, _ = precision_recall_curve(y_true, y_score)
            auc_score = average_precision_score(y_true, y_score)

            name = f"{y_onehot.columns[i]} (AP={auc_score:.2f})"
            fig.add_trace(go.Scatter(x=recall, y=precision, name=name, mode='lines'))

        fig.update_layout(
            title='Precision Recall Curve Plot' ,
            xaxis_title='Recall',
            yaxis_title='Precision',
            yaxis=dict(scaleanchor="x", scaleratio=1),
            xaxis=dict(constrain='domain'),
            width=800, height=800,font=dict(size=18) ,title_x=0.5,
            margin=dict(l=10, r=10, t=100, b=10),
            legend=dict(yanchor='bottom',y=0.01,xanchor='right',x=0.65))
        return fig.show()
        
    def plot_confusion_matrix(self):
        y_scores=self.y_predict_proba
        y_onehot = pd.get_dummies(self.y)
        y_true=np.argmax(y_onehot.values,axis=1)
        y_pred=np.argmax(y_scores,axis=1)
        cm=confusion_matrix(y_true=y_true,y_pred=y_pred)[::-1]
        fig = ff.create_annotated_heatmap(cm, x=self.class_name, y=self.class_name[::-1], annotation_text=cm, showscale=True,colorscale='Viridis')
        fig.update_layout(title='Confusion Matrix Plot\n\n' ,
            xaxis_title='Actual Values',
            yaxis_title='Predicted Values',             
            width=800, height=800,font=dict(size=18),
            title_x=0.5,
            margin=dict(l=10, r=10, t=200, b=10))
        return fig.show()
        
    def plot_classification_report(self):
        y_scores=self.y_predict_proba
        y_onehot = pd.get_dummies(self.y)
        y_true=np.argmax(y_onehot.values,axis=1)
        y_pred=np.argmax(y_scores,axis=1)
        precision=[]
        recall=[]
        f1=[]
        for i in range(len(self.class_name)):
            precision.append(precision_score(y_true,y_pred,average='micro',labels=[i]))
            recall.append(recall_score(y_true,y_pred,average='micro',labels=[i]))
            f1.append(f1_score(y_true,y_pred,average='micro',labels=[i]))
        for j in ['micro','weighted']:
            precision.append(precision_score(y_true,y_pred,average=j))
            recall.append(recall_score(y_true,y_pred,average=j))
            f1.append(f1_score(y_true,y_pred,average=j))
        cr=pd.DataFrame({'Precision':precision,'Recall':recall,'F1-score':f1})
        cr.index=self.class_name+['micro avg','weighted avg']
        cr=cr.round(decimals=2)
        fig = ff.create_annotated_heatmap(cr.values[::-1], x=cr.columns.tolist(), y=cr.index.tolist()[::-1], annotation_text=cr.values[::-1], showscale=True,colorscale='Viridis')
        fig.update_layout(title='Classification Report Plot', 
                   width=800, height=800,font=dict(size=18),title_x=0.5, margin=dict(l=10, r=10, t=200, b=10))
        return fig.show()

    def plot_probability_histogram(self):
        prob_df=pd.DataFrame(self.y_predict_proba,columns=self.class_name)
        fig = px.histogram(prob_df)
        fig.update_layout(
            title='Predicted Probability Histogram Plot',
            xaxis_title='Probability',
            yaxis_title='Count',
            width=1000, height=700,
            font=dict(size=18) ,title_x=0.5,
            margin=dict(l=10, r=10, t=100, b=10),
            legend=dict(yanchor='top',y=0.99,xanchor='right',x=0.99))
        return fig.show()
