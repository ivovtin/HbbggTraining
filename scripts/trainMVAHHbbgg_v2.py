import os
import sys; sys.path.append("/afs/cern.ch/user/i/ivovtin/HHggbb/HHbbgg_ETH/Training/python") # to load packages
import training_utils as utils
import numpy as np
reload(utils)
import preprocessing_utils as preprocessing
reload(preprocessing)
import plotting_utils as plotting
reload(plotting)
import optimization_utils as optimization
reload(optimization)
import postprocessing_utils as postprocessing
reload(postprocessing)
from IPython import get_ipython

ntuples = '2017/flattrees_st_cuts'
#ntuples = '2017'
# "%" sign allows to interpret the rest as a system command
get_ipython().magic(u'env data=$utils.IO.ldata$ntuples')
files = get_ipython().getoutput(u'ls $data | sort -t_ -k 3 -n')
signal = [s for s in files if "output_GluGluToHHTo2B2G_node_SM_13TeV-madgraph_st_cuts.root" in s]
diphotonJets = [s for s in files if "output_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa_st_cuts.root" in s]
gJets_lowPt = [s for s in files if "output_GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts.root" in s]
gJets_highPt = [s for s in files if "output_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts.root" in s]
#gJets_lowPt = [s for s in files if "output_GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_reweight.root" in s]
#gJets_highPt = [s for s in files if "output_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_reweight.root" in s]
#
#signal = [s for s in files if "output_GluGluToHHTo2B2G_node_SM_13TeV-madgraph_st_cuts_ptMjj.root" in s]
#diphotonJets = [s for s in files if "output_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa_st_cuts_ptMjj.root" in s]
##diphotonJets = [s for s in files if "output_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa_st_cuts_reweight_Mjj.root" in s]
#gJets_lowPt = [s for s in files if "output_GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_ptMjj.root" in s]
#gJets_highPt = [s for s in files if "output_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_ptMjj.root" in s]
#
#
#signal = [s for s in files if "output_GluGluToHHTo2B2G_node_SM_13TeV-madgraph_st_cuts_MXcut.root" in s]
#diphotonJets = [s for s in files if "output_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa_st_cuts_MXcut.root" in s]
#gJets_lowPt = [s for s in files if "output_GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_MXcut.root" in s]
#gJets_highPt = [s for s in files if "output_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_MXcut.root" in s]
#
#signal = [s for s in files if "output_GluGluToHHTo2B2G_node_SM_13TeV-madgraph_st_cuts_ptMjj_MXcut.root" in s]
#diphotonJets = [s for s in files if "output_DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa_st_cuts_ptMjj_MXcut.root" in s]
#gJets_lowPt = [s for s in files if "output_GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_ptMjj_MXcut.root" in s]
#gJets_highPt = [s for s in files if "output_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8_st_cuts_ptMjj_MXcut.root" in s]
#

utils.IO.add_signal(ntuples,signal,1)
#utils.IO.add_background(ntuples,bkgr,-1)
utils.IO.add_background(ntuples,diphotonJets,-1)
utils.IO.add_background(ntuples,gJets_lowPt,-2)
utils.IO.add_background(ntuples,gJets_highPt,-2)

for i in range(len(utils.IO.backgroundName)):        
    print "using background file n."+str(i)+": "+utils.IO.backgroundName[i]
for i in range(len(utils.IO.signalName)):    
    print "using signal file n."+str(i)+": "+utils.IO.signalName[i]


#use noexpand for root expressions, it needs this file https://github.com/ibab/root_pandas/blob/master/root_pandas/readwrite.py
#standart of input values 
branch_names = 'absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,PhoJetMinDr,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingJet_DeepCSV,subleadingJet_DeepCSV,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,leadingJet_bRegNNResolution,subleadingJet_bRegNNResolution,noexpand:sigmaMJets/Mjj'.split(",")
#st values with adding pt_gg/m_gg
#branch_names = 'absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,PhoJetMinDr,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingJet_DeepCSV,subleadingJet_DeepCSV,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,leadingJet_bRegNNResolution,subleadingJet_bRegNNResolution,noexpand:sigmaMJets/Mjj,noexpand:leadingPhoton_pt/CMS_hgg_mass,noexpand:subleadingPhoton_pt/CMS_hgg_mass'.split(",")
#st values with adding pt_gg/m_gg, pt_jj/M_jj
#branch_names = 'absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,PhoJetMinDr,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingJet_DeepCSV,subleadingJet_DeepCSV,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,leadingJet_bRegNNResolution,subleadingJet_bRegNNResolution,noexpand:sigmaMJets/Mjj,noexpand:leadingPhoton_pt/CMS_hgg_mass,noexpand:subleadingPhoton_pt/CMS_hgg_mass,noexpand:leadingJet_pt/Mjj,noexpand:subleadingJet_pt/Mjj,PhoJetotherDr'.split(",")

branch_names = [c.strip() for c in branch_names]
print branch_names

import pandas as pd
import root_pandas as rpd
from root_numpy import root2array, list_trees

for i in range(len(utils.IO.backgroundName)):        
    print list_trees(utils.IO.backgroundName[i])
        
preprocessing.set_signals_and_backgrounds("bbggSelectionTree",branch_names)
X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig=preprocessing.set_variables(branch_names)

#np.savetxt('/home/ovtin/cernbox/HHggbb/HHbbgg_ETH_devel/Training/weightssig.txt',weights_sig)
#np.savetxt('/home/ovtin/cernbox/HHggbb/HHbbgg_ETH_devel/Training/weightsbkg.txt',weights_bkg)
#import matplotlib.pyplot as plt
#from xgboost import plot_tree
#from sklearn.metrics import accuracy_score
#plotting.plot_input_variables(X_sig,X_bkg,branch_names)
#plt.show()

#relative weighting between components of one class is kept, all classes normalized to the same
#weights_sig=preprocessing.weight_signal_with_resolution(weights_sig,y_sig)
weights_bkg,weights_sig=preprocessing.normalize_process_weights(weights_bkg,y_bkg,weights_sig,y_sig)

X_bkg,y_bkg,weights_bkg = preprocessing.randomize(X_bkg,y_bkg,weights_bkg)
X_sig,y_sig,weights_sig = preprocessing.randomize(X_sig,y_sig,weights_sig)

print X_bkg.shape
print y_bkg.shape
#bbggTrees have by default signal and CR events, let's be sure that we clean it
X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig=preprocessing.clean_signal_events(X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig)
print X_bkg.shape
print y_bkg.shape

y_total_train = preprocessing.get_total_training_sample(y_sig,y_bkg).ravel()
X_total_train = preprocessing.get_total_training_sample(X_sig,X_bkg)

y_total_test = preprocessing.get_total_test_sample(y_sig,y_bkg).ravel()
X_total_test = preprocessing.get_total_test_sample(X_sig,X_bkg)

w_total_train = preprocessing.get_total_training_sample(weights_sig,weights_bkg).ravel()
w_total_test = preprocessing.get_total_test_sample(weights_sig,weights_bkg).ravel()


########final optimization with all fixed#######

from sklearn.externals import joblib
import xgboost as xgb
from sklearn.metrics import mean_squared_error

#X_all = preprocessing.cut_region(utils.IO.signalName[0],"tagsDumper/trees/GluGluToHHTo2B2G_node_SM_13TeV_madgraph_13TeV_DoubleHTag_0",branch_names,features,cuts)

#clf = xgb.XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=1,
#       gamma=0, learning_rate=0.1, max_delta_step=0, max_depth=5,
#       min_child_weight=1e-05, missing=None, n_estimators=1500, nthread=20,
#       objective='binary:logistic', reg_alpha=0, reg_lambda=0.1,
#       scale_pos_weight=1, seed=0, silent=True, subsample=1)
#
#basic
params = {'base_score': 0.5, 'colsample_bylevel': 1, 'colsample_bytree': 1,
       'gamma': 0, 'learning_rate': 0.1, 'max_delta_step': 0, 'max_depth': 10,
       'min_child_weight': 1e-05, 'missing': None, 'n_estimators': 2000, 'nthread': 20,
       'objective': 'binary:logistic', 'reg_alpha': 0, 'reg_lambda': 0.1,
       'scale_pos_weight': 1, 'seed': 0, 'silent': True, 'subsample': 1 }
#
#1 -
#params = {'base_score': 0.5, 'colsample_bylevel': 1, 'colsample_bytree': 1,
#       'gamma': 0, 'learning_rate': 0.1, 'max_delta_step': 0, 'max_depth': 10,
#       'min_child_weight': 1e-05, 'missing': None, 'n_estimators': 1500, 'nthread': 20,
#       'objective': 'binary:logistic', 'reg_alpha': 0.0, 'reg_lambda': 0.01,
#       'scale_pos_weight': 1, 'seed': 0, 'silent': True, 'subsample': 1 }
#2 -
#params = {'base_score': 0.5, 'colsample_bylevel': 1, 'colsample_bytree': 1,
#       'gamma': 0, 'learning_rate': 0.01, 'max_delta_step': 0, 'max_depth': 10,
#       'min_child_weight': 1e-05, 'missing': None, 'n_estimators': 1500, 'nthread': 20,
#       'objective': 'binary:logistic', 'reg_alpha': 0.0, 'reg_lambda': 0.01,
#       'scale_pos_weight': 1, 'seed': 0, 'silent': True, 'subsample': 1 }
#params = {'base_score': 0.5, 'booster':'gbtree', 'colsample_bylevel': 1, 'colsample_bytree': 1,
#       'gamma': 0, 'learning_rate': 0.01, 'max_delta_step': 0, 'max_depth': 5,
#       'min_child_weight': 1e-05, 'missing': None, 'n_estimators': 2000, 'n_jobs':1, 'nthread': 12,
#       'objective': 'binary:logistic', 'random_state':0, 'reg_alpha': 0, 'reg_lambda': 1,
#       'scale_pos_weight': 1, 'seed': 0, 'silent': True, 'subsample': 1 }
#params = {'base_score': 0.5, 'colsample_bylevel': 1, 'colsample_bytree': 1,
#       'gamma': 0, 'learning_rate': 0.1, 'max_delta_step': 0, 'max_depth': 3,
#       'min_child_weight': 1e-05, 'missing': None, 'n_estimators': 1000, 'nthread': 12,
#       'objective': 'binary:logistic', 'reg_alpha': 0, 'reg_lambda': 0.1,
#       'scale_pos_weight': 1, 'seed': 0, 'silent': True, 'subsample': 1 }
#params = {'base_score': 0.5, 'colsample_bylevel': 1, 'colsample_bytree': 1,
#       'gamma': 0, 'learning_rate': 0.1, 'max_delta_step': 0, 'max_depth': 3,
#       'min_child_weight': 1e-05, 'missing': None, 'n_estimators': 40, 'nthread': 20,
#       'objective': 'binary:logistic', 'reg_alpha': 0, 'reg_lambda': 0.1,
#       'scale_pos_weight': 1, 'seed': 0, 'silent': True, 'subsample': 1 }
clf = xgb.XGBClassifier(**params)
eval_set = [(X_total_train, y_total_train), (X_total_test, y_total_test)]
#clf.fit(X_total_train, y_total_train, sample_weight=w_total_train, eval_set=eval_set, eval_metric=["error", "logloss", "auc"], verbose=True)
#For multiclass
clf.fit(X_total_train, y_total_train, sample_weight=w_total_train, eval_set=eval_set, eval_metric=["merror","mlogloss"], verbose=True)
#clf.fit(X_total_train,y_total_train, sample_weight=w_total_train)
mse = mean_squared_error(y_total_test, clf.predict(X_total_test))
print("MSE: %.4f" % mse)
#clf.evals_result()
print clf.score(X_total_train,y_total_train)
#print clf.best_params_
joblib.dump(clf, os.path.expanduser('/eos/user/i/ivovtin/HHggbb/HHbbgg_ETH_devel/Training/plots/optimization/simlple_Test_binary_st.pkl'), compress=9)


import matplotlib.pyplot as plt
from xgboost import plot_tree
from sklearn.metrics import accuracy_score

#plotting.plot_input_variables(X_sig,X_bkg,branch_names)
#plt.show()
plotting.plot_classifier_output(clf,X_total_train,X_total_test,y_total_train,y_total_test,outString="xbrg_test_st_values_notcut")
#plt.show()

#fpr,tpr = plotting.plot_roc_curve(X_total_train,y_total_train,clf)
#plotting.print_roc_report(fpr,tpr)
#plt.savefig(utils.IO.plotFolder+"ROC_train.eps")
#plt.show()
#fpr,tpr = plotting.plot_roc_curve(X_total_test,y_total_test,clf)
#plotting.print_roc_report(fpr,tpr)
#plt.show()

plt.bar(range(len(clf.feature_importances_)), clf.feature_importances_)
plt.savefig(utils.IO.plotFolder+"importance1.eps")
#plt.show()
#
xgb.plot_importance(clf)
plt.savefig(utils.IO.plotFolder+"importance2.eps")
#plt.show()

fpr_dipho_2ndtest_2,tpr_dipho_2ndtest_2 = plotting.plot_roc_curve_multiclass_singleBkg(X_total_test,y_total_test,clf,-1,1,"test_xgbr_diphotons_st_cuts",weights=w_total_test)
plotting.print_roc_report(fpr_dipho_2ndtest_2,tpr_dipho_2ndtest_2,outString="test_xgbr_diphotons_st_cuts")
plt.savefig(utils.IO.plotFolder+"test_xgbr_diphotons_st_cuts.eps")
#plt.show()
fpr_gJets_2ndtest_2,tpr_gJets_2ndtest_2 = plotting.plot_roc_curve_multiclass_singleBkg(X_total_test,y_total_test,clf,-2,1,"test_xgbr_gJets_st_cuts",weights=w_total_test)
plotting.print_roc_report(fpr_gJets_2ndtest_2,tpr_gJets_2ndtest_2,outString="test_xgbr_gJets_st_cuts")
plt.savefig(utils.IO.plotFolder+"test_xgbr_gJets_st_cuts.eps")
#plt.show()

fpr_dipho_2ndtrain_2,tpr_dipho_2ndtrain_2 = plotting.plot_roc_curve_multiclass_singleBkg(X_total_train,y_total_train,clf,-1,1,"train_xgbr_diphotons_st_cuts",weights=w_total_train)
plotting.print_roc_report(fpr_dipho_2ndtrain_2,tpr_dipho_2ndtrain_2,outString="train_xgbr_diphotons_st_cuts")
plt.savefig(utils.IO.plotFolder+"train_xgbr_diphotons_st_cuts.eps")
#plt.show()
fpr_gJets_2ndtrain_2,tpr_gJets_2ndtrain_2 = plotting.plot_roc_curve_multiclass_singleBkg(X_total_train,y_total_train,clf,-2,1,"train_xgbr_gJets_st_cuts",weights=w_total_train)
plotting.print_roc_report(fpr_gJets_2ndtrain_2,tpr_gJets_2ndtrain_2,outString="train_xgbr_gJets_st_cuts")
plt.savefig(utils.IO.plotFolder+"train_xgbr_gJets_st_cuts.eps")
#plt.show()

# #############################################################################
#
# Plot feature importance
#importances = clf.get_fscore()
importances = clf.get_booster().get_score(importance_type='weight')
importance_frame = pd.DataFrame({'Importance': list(importances.values()), 'Feature': list(importances.keys())})
importance_frame.sort_values(by = 'Importance', inplace = True)
importance_frame.plot(kind = 'barh', x = 'Feature', figsize = (8,8), color = 'orange')
#
# make predictions for test data
y_pred = clf.predict(X_total_test)
predictions = [round(value) for value in y_pred]    
# evaluate predictions
accuracy = accuracy_score(y_total_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

## retrieve performance metrics
results = clf.evals_result()
epochs = len(results['validation_0']['merror'])
x_axis = range(0, epochs)
## plot log loss
fig, ax = plt.subplots()
ax.plot(x_axis, results['validation_0']['mlogloss'], label='Train')
ax.plot(x_axis, results['validation_1']['mlogloss'], label='Test')
ax.legend()
plt.ylabel('Log Loss')
plt.title('XGBoost Log Loss')
plt.savefig(utils.IO.plotFolder+"XGBoostLogLoss.eps")
#plt.show()
## plot classification error
fig, ax = plt.subplots()
ax.plot(x_axis, results['validation_0']['merror'], label='Train')
ax.plot(x_axis, results['validation_1']['merror'], label='Test')
ax.legend()
plt.ylabel('Classification Error')
plt.title('XGBoost Classification Error')
plt.savefig(utils.IO.plotFolder+"XGBoostClassificationError.eps")
#plt.show()

