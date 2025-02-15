import os, copy
from ROOT import gStyle, TCanvas, TLegend, TH1F, gROOT, TFile
from common.officialStyle import officialStyle
#from common.DisplayManager_postfit import DisplayManager
#from common.DataMCPlot import *


gROOT.SetBatch(True)
#gROOT.SetBatch(False)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


#shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/dev/datacard_MUSF_blind/tau_rhomass_unrolled_coarse_new.root'
<<<<<<< HEAD
shape_file = '/work/cgalloni/Rjpsi_analysis/CMSSW_10_2_10/src/rJpsi/anal/datacard_fromYuta20220317_sr4p3_sb2p5-3p5_lp2-2p5_fixed_Federica/sr/tau_rhomass_unrolled_new.root'
file_shape = TFile(shape_file)
data_sb = file_shape.Get('sb/data_obs')
nbin = data_sb.GetXaxis().GetNbins()
=======
#shape_file = '/work/ytakahas/work/analysis/CMSSW_10_2_10/src/rJpsi/anal/dev/datacard_MUSF_blind/tau_rhomass_unrolled_new.root'
#file_shape = TFile(shape_file)
#data_sb = file_shape.Get('sb/data_obs')
#nbin = data_sb.GetXaxis().GetNbins()
>>>>>>> origin/main



filename = 'output/sm_cards/LIMITS/fitDiagnostics.root'

file = TFile(filename)

print file

process = {
    'data':{'name':'data'},
    'total_signal':{'name':'total_signal'},
    'total_background':{'name':'total_background'}
}

#for ibin in range(1, nbin+1):
#    process['bg_bin' + str(ibin)] = {'name':'bg_bin' + str(ibin)}


ensureDir('Plots/')

#nbin = 20

for ftype in ['fit_s', 'prefit']:
#for ftype in ['prefit', 'fit_b']:


    for cr in ['rJpsi_sr_1_2018']:
#    for cr in ['sr', 'sb']:
#    for cr in ['rJpsi_sr_1_2018']:

        hists = {}
    
        ymax = -1

        
        for ii, var in process.iteritems():
    
            hist = file.Get('shapes_' + ftype + '/' + cr + '/' + var['name'])
            
#            print hist, 'shapes_' + ftype + '/' + cr + '/' + var['name']

            hist.SetFillStyle(0)
#            print file
            
            nbin = hist.GetXaxis().GetNbins()
#            print nbin
            
#            if var['name'].find('bin')!=-1:
#                hist.SetLineColor(2)
#                hist.SetLineStyle(2)

            if ii.find('signal')!=-1:
                hist.SetLineColor(2)
                hist.SetLineStyle(2)
            elif ii.find('data')!=-1:
                hist.SetMarkerStyle(20)
                hist.SetMarkerSize(1)

            hist.SetLineWidth(3)
        
            hists[ii] = copy.deepcopy(hist)

            if ymax < hist.GetMaximum(): ymax = hist.GetMaximum()

            
        canvas = TCanvas('canvas_' + ftype + '_' + cr)
#        canvas.SetLogy()

        frame = TH1F('frame_' + ftype + '_' + cr, 'fname_' + ftype + '_' + cr, nbin, 0, nbin)
        frame.GetXaxis().SetTitle('Tau rhomasses unrolled bin ID')
        frame.GetYaxis().SetTitle('Events')
  
#        if ftype.find('prefit')!=-1:
        frame.SetMaximum(ymax*2.)
        frame.SetMinimum(0.)
#        else:
#            frame.SetMaximum(ymax*8)
#            frame.SetMinimum(0.8)

        frame.Draw()

        hs = copy.deepcopy(hists['total_background'])
        hs.Add(copy.deepcopy(hists['total_signal']))
        hs.SetFillStyle(1)
        hs.SetFillColor(2)
        hs.SetLineColor(2)
        hs.Draw('hsame')

        hists['total_background'].SetFillStyle(1)
        hists['total_background'].SetFillColor(10)
        hists['total_background'].Draw('hsame')
        
        hists['total_signal'].Draw('hsame')
        hists['data'].Draw('epzsame')

        canvas.RedrawAxis()                
        canvas.SaveAs('Plots/' + ftype + '_' + cr + '.gif')
