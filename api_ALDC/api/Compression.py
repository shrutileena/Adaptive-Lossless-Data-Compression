from flask_restful import Resource
from flask import request
import os
from app import app
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2

VALID_FILE_EXTENSIONS = ['txt','png','jpg','jpeg']
LETTER_IDX = pickle.load(open('letter_idx.pickle','rb'))
IDX_LETTER = {value:key for key,value in LETTER_IDX.items()}
IDX_LETTER[0] = ''

class Compression(Resource):
    def __init__(self):
        latent_dim = 128
        self.model = tf.keras.models.load_model('s2s.h5')
        encoder_inputs = self.model.input[0]  # input_1
        encoder_outputs, state_h_enc, state_c_enc = self.model.layers[2].output  # lstm_1
        encoder_states = [state_h_enc, state_c_enc]
        self.encoder_model = keras.Model(encoder_inputs, encoder_states)

        decoder_inputs = self.model.input[1]  # input_2
        decoder_state_input_h = keras.Input(shape=(latent_dim,), name="input_3")
        decoder_state_input_c = keras.Input(shape=(latent_dim,), name="input_4")
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_lstm = self.model.layers[3]
        decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
            decoder_inputs, initial_state=decoder_states_inputs
        )
        decoder_states = [state_h_dec, state_c_dec]
        decoder_dense = self.model.layers[4]
        decoder_outputs = decoder_dense(decoder_outputs)
        self.decoder_model = keras.Model(
            [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
        )
    def is_valid_file(self,filename):
        return filename.split('.')[-1] in VALID_FILE_EXTENSIONS
    
    def file_type(self,filename):
        if self.is_valid_file(filename):
            if filename.split('.')[-1] in ['png','jpg','jpeg']:
                return 'img'
            else:
                return 'txt'
        return False

    def compress(self,inp):
        l = len(inp)
        sv = self.encoder_model.predict(inp)
        target_seq = np.zeros((l,1,131))
        for i in range(l):
            target_seq[i,0,129] = 1.0
        k = 0
        y = np.zeros((l,47))
        while k<47:
            output_token,h,c = self.decoder_model.predict([target_seq]+sv)
            sti = []
            for i in range(l):
                sampled_token_index = np.argmax(output_token[i,-1,:])
                sti.append(sampled_token_index)
                y[i][k] = sampled_token_index
            k += 1
            target_seq = np.zeros((l,1,131))
            for i in range(l):
                target_seq[i,0,sti[i]] = 1.0
            sv = [h,c]
        return y


    def get(self):
        pass

    def post(self):
        if request.method == 'POST':
            length = 0
            len_c = 0
            file = request.files['file']
            filename = file.filename
            fileType = self.file_type(filename)
            if fileType:
                type = fileType
            else:
                return {'done':'Bad Request'}

            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(filepath)
            
            if type == 'txt':
                with open(filepath,'r',encoding='utf-8') as f:
                    data = f.read()
                with open(filepath,'w+',encoding='utf-8') as f:
                    f.write(data)
                print(data)
                print(len(data))
                x = []
                z = ''
                length = len(data)
                for i in data:
                    z = z + str(LETTER_IDX[i]) + ' '

                l = z.split(' ')
                for i in range(0,len(l),49):
                    x.append(l[i:i+49])

                ori = np.zeros((len(x),49,131))
                for idx,i in enumerate(x):
                    for t,char in enumerate(i):
                        if char != '':
                            ori[idx,t,int(char)] = 1.0
                    
                pred = self.compress(ori)
                z = ''
                
                for i in pred:
                    for j in i:
                        if int(j) == 130:
                            z += '\n'
                        else:
                            z += IDX_LETTER[int(j)]
                print(z)
                print(len(z))
                len_c = len(z)

                with open(f'compressed files/{filename}','w+',encoding='utf-8') as f:
                    f.write(z)
                
            if type == 'img':
                img = cv2.imread(filepath)
                print(img.shape)
                img = img.flatten()
                print(len(img))
                length = len(img)

                img = (img // 255) * 128
                img = np.array(img,dtype='int32')
                x = []
                for i in range(0,len(img),49):
                    x.append(img[i:i+49])
                ori = np.zeros((len(x),49,131))
                for idx,i in enumerate(x):
                    for t,char in enumerate(i):
                        if char != '':
                            ori[idx,t,int(char)] = 1.0

                pred = self.compress(ori)
                z = ''

                for i in pred:
                    for j in i:
                        if int(j) == 130:
                            z += '\n'
                        else:
                            z += IDX_LETTER[int(j)]
                
                with open(f'compressed files/{filename}','w+',encoding='utf-8') as f:
                    f.write(z)
                len_c = len(z)

            return {'done':True, "len": length, "len_c": len_c}