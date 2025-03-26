#!/usr/bin/env python
import os
import time
import subprocess





dbTagSuffix="_UPC2023_v1"
outputFile ="UPC_2023_311024"
regres_dir = "/eos/cms/store/group/phys_heavyions/anstahll/CERN/PbPb2023/Regression_Final/"
regres_data = [
    {"filename" : "resultsSCV1_Run3_2023_UPC/Run3_2023_UPC_IdealIC_IdealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root",  "dbLabel" : "pfscecal_{region_lower}Correction_offline_v2","fileLabel" : "{region}Correction"},
    {"filename" : "resultsSCV1_Run3_2023_UPC/Run3_2023_UPC_RealIC_RealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root",  "dbLabel" : "pfscecal_{region_lower}Uncertainty_offline_v2","fileLabel" : "{region}Uncertainty"},

    {"filename" : "resultsPhoV1_Run3_2023_UPC/regPhoEcalRun3_2023_UPC_IdealIC_IdealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root",  "dbLabel" : "photon_{region_lower}_ecalOnly_1To20_0p2To2_mean","fileLabel" : "{region}Correction"},
    {"filename" : "resultsPhoV1_Run3_2023_UPC/regPhoEcalRun3_2023_UPC_RealIC_RealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root",  "dbLabel" : "photon_{region_lower}_ecalOnly_1To20_0p0002To0p5_sigma","fileLabel" : "{region}Uncertainty"},

    {"filename" : "resultsEleV1_Run3_2023_UPC_LowPtGsdEle/regEleEcalRun3_2023_UPC_LowPtGsdEle_IdealIC_IdealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "lowPtElectron_{region_lower}_ecalOnly_1To20_0p2To2_mean","fileLabel" : "{region}Correction"},
    {"filename" : "resultsEleV1_Run3_2023_UPC_LowPtGsdEle/regEleEcalRun3_2023_UPC_LowPtGsdEle_RealIC_RealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "lowPtElectron_{region_lower}_ecalOnly_1To20_0p0002To0p5_sigma","fileLabel" : "{region}Uncertainty"},
    {"filename" : "resultsEleV1_Run3_2023_UPC_LowPtGsdEle/regEleEcalTrkRun3_2023_UPC_LowPtGsdEle_RealIC_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "lowPtElectron_{region_lower}_ecalTrk_1To20_0p2To2_mean","fileLabel" : "{region}Correction"},
    {"filename" : "resultsEleV1_Run3_2023_UPC_LowPtGsdEle/regEleEcalTrkRun3_2023_UPC_LowPtGsdEle_RealIC_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "lowPtElectron_{region_lower}_ecalTrk_1To20_0p0002To0p5_sigma","fileLabel" : "{region}Uncertainty"}, 

    {"filename" : "resultsEleV1_Run3_2023_UPC/regEleEcalRun3_2023_UPC_IdealIC_IdealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "electron_{region_lower}_ecalOnly_1To20_0p2To2_mean","fileLabel" : "{region}Correction"},
    {"filename" : "resultsEleV1_Run3_2023_UPC/regEleEcalRun3_2023_UPC_RealIC_RealTraining_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "electron_{region_lower}_ecalOnly_1To20_0p0002To0p5_sigma","fileLabel" : "{region}Uncertainty"},
    {"filename" : "resultsEleV1_Run3_2023_UPC/regEleEcalTrkRun3_2023_UPC_RealIC_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "electron_{region_lower}_ecalTrk_1To20_0p2To2_mean","fileLabel" : "{region}Correction"},
    {"filename" : "resultsEleV1_Run3_2023_UPC/regEleEcalTrkRun3_2023_UPC_RealIC_stdVar_stdCuts_{region}_ntrees1500_results.root", "dbLabel" : "electron_{region_lower}_ecalTrk_1To20_0p0002To0p5_sigma","fileLabel" : "{region}Uncertainty"},
]
    
if os.path.isfile(outputFile+".db"):
    print("file ",outputFile+".db","exists, deleting in 10s")
    time.sleep(10)
    os.remove(outputFile+".db")


toget_str = ""
labeltag_str = ""

for entry in regres_data:
    for region in ["EB","EE"]:
        filename = entry["filename"].format(region=region)
        dbLabel = entry["dbLabel"].format(region_lower=region.lower())
        fileLabel = entry["fileLabel"].format(region=region)
        cmd = "cmsRun ../gbrForestDBWriter.py gbrFilename={filename} fileLabel={fileLabel} dbLabel={dbLabel} dbFilename={dbFilename} dbTag={dbTag}".format(filename=regres_dir+filename,fileLabel=fileLabel,dbLabel=dbLabel,dbTag=dbLabel+dbTagSuffix,dbFilename=outputFile)
        print(cmd)
        subprocess.Popen(cmd.split()).communicate()
        toget_str += """cms.PSet(record = cms.string("GBRDWrapperRcd"),
         label = cms.untracked.string("{label}"),
         tag = cms.string("{tag}")),
""".format(label=dbLabel,tag=dbLabel+dbTagSuffix)
        labeltag_str+="{} {}\n".format(dbLabel+dbTagSuffix,dbLabel)

print(toget_str)
print(labeltag_str)
