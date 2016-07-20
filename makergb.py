import numpy as np
import img_scale
import astropy.stats as astats

# RGB image with flexible scaling of color of the brightest pixels
def makeRGB(rimg,gimg,bimg,minsigma=1.,maxpercentile=99.9,color_scaling=None,sigmaclip=3,iters=20,nonlinear=8.):
    ''' minsigma -- black level is set this many clipped-sigma below sky
       maxpercentile -- white level is set at this percentile of the pixel levels
       color_scaling -- list or array: maximum value is divided by this; 
                        so if you want the brightest pixels to be reddish, try, say 1.0,0.2, 0.1
       sigmaclip -- clipping threshold for iterative sky determination
       iters -- number of iterations for iterative sky determination
    '''
    bands = ['r','g','b']
    # Color scaling
    if color_scaling == None:
        cfactor = {'r':1.,'g':1.0,'b':1.0}
    else:
        cfactor = {}
        for i,b in enumerate(bands):
            cfactor[b] = color_scaling[i]
    images = {'r':rimg, 'g':gimg, 'b':bimg}
    rescaled_img = {}
    for b in ['r','g','b']:
        mean, median, stddev = astats.sigma_clipped_stats(images[b],sigma=sigmaclip,iters=iters)
        imin = median-minsigma*stddev
        imax = np.percentile(images[b],maxpercentile)
        rescaled_img[b] = img_scale.asinh(images[b],scale_min=imin,scale_max=imax/cfactor[b],non_linear=nonlinear)
        print imin,imax
    rgbimg = np.zeros((rescaled_img['r'].shape[0],rescaled_img['r'].shape[1],3),dtype=np.float64)
    rgbimg[:,:,0]=rescaled_img['r']
    rgbimg[:,:,1]=rescaled_img['g']
    rgbimg[:,:,2]=rescaled_img['b']
    return rgbimg
