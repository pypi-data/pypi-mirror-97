import numpy as np
import SimpleITK as sitk 
from skimage.measure import label
#from radiomics.featureextractor import RadiomicsFeatureExtractor
import matplotlib.pyplot as plt
import scipy as sc
from sklearn import mixture
from library_dicom.post_processing.PostProcess_Reader import PostProcess_Reader

class GaussianModel(PostProcess_Reader) :


    def __init__(self, mask_path, pet_path, type) : 
        super().__init__(mask_path, pet_path, type)
        self.parameters = self.gaussien_mixture_model()


    def gaussien_mixture_model(self) : 
        parameters = {}
        for key in range(1, len(self.features) + 1) : 
            subdict = {}
            X_train = np.asarray(self.features[key]['suv_values']).reshape((-1,1))
            #si volume plus petit que 30ml, on laisse
            if self.features[key]['volume'] < float(30) : 

                lowest_bic = np.infty
                bic = []
                for cv_type in cv_types : 
                    gmm = mixture.GaussianMixture(n_components= 1, covariance_type=cv_type, random_state = 0)
                    gmm.fit(X_train)
                    bic.append(gmm.bic(X_train))
                    if bic[-1] < lowest_bic : 
                        lowest_bic = bic[-1]
                        best_gmm = gmm 
                        best_n_components = 1
                        best_cv_type = cv_type
                        labels = best_gmm.predict(X_train) #ndarray

                subdict['best_n_components'] = best_n_components
                subdict['best_cv_type'] = best_cv_type
                subdict['label'] = labels

                parameters[key] = subdict

            else : 

                #find best parameters for model 

                lowest_bic = np.infty
                bic = []
                n_components_range = range(1, 8)
                cv_types = ['spherical', 'tied', 'diag', 'full']
                for cv_type in cv_types : 
                    for n_components in n_components_range : 
                        gmm = mixture.GaussianMixture(n_components=n_components, covariance_type=cv_type, random_state = 0)
                        gmm.fit(X_train)
                        bic.append(gmm.bic(X_train))
                        if bic[-1] < lowest_bic : 
                            lowest_bic = bic[-1]
                            best_gmm = gmm 
                            best_n_components = n_components
                            best_cv_type = cv_type
                            labels = best_gmm.predict(X_train) #ndarray
                            
                subdict['best_n_components'] = best_n_components
                subdict['best_cv_type'] = best_cv_type
                subdict['label'] = labels

                parameters[key] = subdict

        return parameters


    def get_histogram_best_model(self, label):
        X_train = np.asarray(self.features[label]['suv_values']).reshape((-1,1))
        n_components = self.parameters[label]['best_n_components']
        cv_type = self.parameters[label]['best_cv_type']

        gmm = mixture.GaussianMixture(n_components=n_components, covariance_type=cv_type, random_state = 0)
        gmm.fit(X_train)

        gmm_x = np.linspace(0, np.max(X_train), X_train.shape[0])
        gmm_y = np.exp(gmm.score_samples(gmm_x.reshape(-1,1)))

        plt.hist(self.features[label]['suv_values'], bins = 'fd', normed = True, alpha = 0.6, label = 'suv_value')
        plt.xlabel('suv_value')
        plt.ylabel('frequency')
            
        plt.plot(gmm_x, gmm_y, label = 'gmm model', color = 'mediumvioletred', lw = 2)
        plt.title('roi :{}, n_components : {} , cv_type : {}'.format(label, n_components, cv_type))
        plt.legend()
        plt.show()


    def get_index_cluster(self, list_labels, n_components): #for 1 roi 
        liste = []
        for i in range(n_components) : 
            liste.append(np.where(list_labels == i))

        return liste 

    def number_of_roi_after_model(self) : 
        number_of_roi = len(self.features)
        number_total_of_roi = 0
        for key in range(1, number_of_roi + 1) : 
            new_labels = self.get_index_cluster(self.parameters[key]['label'], self.parameters[key]['best_n_components'])
            number_total_of_roi += len(new_labels)

        return np.arange(1, number_total_of_roi+1)

    def new_clusters(self):
        number_of_roi = len(self.features)
        new_clusters = []
        for key in range(1, number_of_roi + 1) : 
            x,y,z = self.features[key]['coordonate']
            liste_new_labels = self.get_index_cluster(self.parameters[key]['label'], self.parameters[key]['best_n_components'])
            for liste in liste_new_labels : 
                subliste = []
                for index in liste[0] : 
                    subliste.append([x[index], y[index], z[index]])

                new_clusters.append(subliste)

        return new_clusters

    def new_labelled_mask(self):
        shape_labelled_mask = self.labelled_mask.shape
        labelled_mask = np.zeros((shape_labelled_mask[0], shape_labelled_mask[1], shape_labelled_mask[2]))
        liste_new_labels = self.number_of_roi_after_model()
        coordonate_new_clusters = self.new_clusters()
        for liste, label in zip(coordonate_new_clusters, liste_new_labels) :
            for index in liste : 
                labelled_mask[index[0], index[1], index[2]] = label

        return labelled_mask.astype(np.uint8)



    

