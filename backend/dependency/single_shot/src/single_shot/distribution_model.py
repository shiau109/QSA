from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
import numpy as np

import time


class GMM_model():

    def __init__( self ):
        self.gmm = GaussianMixture(n_components=2, random_state=0)

    def import_trainingData( self, data ):
        """
        input numpy array with shape (n,2)
        n is point number
        """
        self.training_data = data
        self.gmm.fit(data)
        self.gmm.weights_ = [0.5,0.5]

        # return self
    def relabel_model( self, ground_data ):
        """
        input numpy array with shape (2,n)
        """
        print( ground_data.shape )

        gp = np.array([np.mean(ground_data, axis=1)])
        print( gp )
        print( gp.shape )

        print(self.gmm.predict( gp ))
        if self.gmm.predict( gp ) == 1:
            self.gmm.means_ = np.flip(self.gmm.means_,0)
            self.gmm.weights_ = np.flip(self.gmm.weights_,0)
            self.gmm.covariances_ = np.flip(self.gmm.covariances_,0)
            self.gmm.precisions_cholesky_ = np.flip(self.gmm.precisions_cholesky_,0)

    def output_paras( self ):
        """
        four para in dict
        means
        weights
        covariances
        precisions_cholesk
        """
        output_dict = {
            "means":self.gmm.means_,
            "weights":self.gmm.weights_,
            "covariances":self.gmm.covariances_,
            "precisions_cholesky":self.gmm.precisions_cholesky_,
        }

        return output_dict

    def rebuild_model( self, paras:dict ):

        self.gmm.means_ = paras["means"]
        self.gmm.weights_ = paras["weights"]
        self.gmm.covariances_ = paras["covariances"]
        self.gmm.precisions_cholesky_ = paras["precisions_cholesky"]


    def get_prediction( self, data ):
        """
        input numpy array with shape (n,2)
        n is point number
        """
        self.__input_data = data
        self.__predict_label = self.gmm.predict( data )
        return self.__predict_label

    def get_label( self ):
        """
        input numpy array with shape (n,2)
        n is point number
        """

        return self.__predict_label

    def get_distribution( self ):

        return np.bincount(self.__predict_label)


### KMeans_model Not finished yet
class KMeans_model():

    def __init__( self ):
        self.kmeans = KMeans(n_components=2, random_state=0)

    def training( self, data ):
        """
        input numpy array with shape (n,2)
        n is point number
        """
        self.__training_data = data
        self.gmm.fit(data)

        # return self

    def output_paras( self ):
        """
        four para in dict
        means
        weights
        covariances
        precisions_cholesk
        """
        output_dict = {
            "means":self.gmm.means_,
            "weights":self.gmm.weights_,
            "covariances":self.gmm.covariances_,
            "precisions_cholesky":self.gmm.precisions_cholesky_,
        }

        return output_dict

    def rebuild_model( self, paras:dict ):

        self.gmm.means_ = paras["means"]
        self.gmm.weights_ = paras["weights"]
        self.gmm.covariances_ = paras["covariances"]
        self.gmm.precisions_cholesky_ = paras["precisions_cholesky"]


    def predict_data( self, data ):
        """
        input numpy array with shape (n,2)
        n is point number
        """
        self.__input_data = data
        self.__predict_lable = self.gmm.predict( data )

    def get_label( self ):
        """
        input numpy array with shape (n,2)
        n is point number
        """

        return self.__predict_lable

    def get_distribution( self ):

        return np.bincount(self.__predict_lable)