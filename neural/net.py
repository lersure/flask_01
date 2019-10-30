import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import matplotlib.pyplot as plt
import pickle

model_path = '../neuralTest/model.ckpt'
reader = tf.train.NewCheckpointReader(model_path)
all_variables = reader.get_variable_to_shape_map()
print(all_variables)

conv1_weight = reader.get_tensor("C1-conv/weight")
# print(conv1_weight.shape)                         #deng
# 计算每个kernel权重的和 (也可以使用其他指标，如std，mean等)
conv1_weight_sum = np.sum(conv1_weight, (0, 1, 2))
sort_conv1_weights = np.sort(conv1_weight_sum)
# 绘制conv1的
x = np.arange(0, len(sort_conv1_weights), step=1)
plt.plot(x, sort_conv1_weights)
plt.show()  # 显示绘制的C1conv_weights的分布图像

pure_conv1_weight_index = np.where(conv1_weight_sum >= sort_conv1_weights[8])
pure_conv1_weight = conv1_weight[:, :, :, pure_conv1_weight_index[0]]
# conv1对应的bias 也做相同处理
conv1_bias = reader.get_tensor("C1-conv/bias")
pure_conv1_bias = conv1_bias[pure_conv1_weight_index[0]]

print(pure_conv1_bias)

conv3_weight = reader.get_tensor("C3-conv/weight")
conv3_bias = reader.get_tensor("C3-conv/bias")
conv3_weight = conv3_weight[:, :, pure_conv1_weight_index[0], :]
print(conv3_weight.shape)

# 同理先计算每个kernel 的权重和 找到最无关的一些kernel
conv3_weight_sum = np.sum(conv3_weight, (0, 1, 2))
sort_conv3_weights = np.sort(conv3_weight_sum)

# 绘制conv3的权重和分布图
x = np.arange(0, len(sort_conv3_weights), step=1)
plt.plot(x, sort_conv3_weights)
plt.show()

conv3_weight_std = np.std(conv3_weight, (0, 1, 2))
sort_conv3_weights_std = np.sort(conv3_weight_std)
# 绘制conv3的权重std分布图
x = np.arange(0, len(sort_conv3_weights_std), step=1)
plt.plot(x, sort_conv3_weights_std)
plt.show()

pure_conv3_weight_index = np.where(conv3_weight_std >= sort_conv3_weights_std[8])
pure_conv3_weight = conv3_weight[:, :, :, pure_conv3_weight_index[0]]
pure_conv3_weight.shape
# conv3对应的bias 也做相同处理
pure_conv3_bias = conv3_bias[pure_conv3_weight_index[0]]
pure_conv3_bias

channel_dict = {'conv1': pure_conv1_weight.shape[-1], 'conv3': pure_conv3_weight.shape[-1]}

pure_weights = {'conv1/weights': pure_conv1_weight, 'conv1/biases': pure_conv1_bias,
                'conv3/weights': pure_conv3_weight, 'conv3/biases': pure_conv3_bias, }

all_data = {}
all_data['channel_dict'] = channel_dict
all_data['pure_weights'] = pure_weights

with open('./pure_1.pb', 'wb') as f:
    pickle.dump(all_data, f)

with open('./pure_1.pb', 'rb') as f:
    load = pickle.load(f)

channel_dict = load['channel_dict']
pure_weights = load['pure_weights']
print('channel dict:'.format(str(channel_dict)))
print('channel dict:'.format(str(pure_weights)))

# conv1_weights = tf.get_variable('weight', [5, 5, 1, 32],
#                                         initializer=tf.truncated_normal_initializer(stddev=0.1))
# conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1, 1, 1, 1], padding='SAME')
#
# pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
#
# conv2_weights = tf.get_variable('weight', [5, 5, 32, 64],
#                                         initializer=tf.truncated_normal_initializer(stddev=0.1))
# conv2 = tf.nn.conv2d(pool1, conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
#
# pool2 = tf.nn.max_pool(relu2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# saver = tf.train.import_meta_graph('./model.ckpt.meta')  # 加载图结构
# gragh = tf.get_default_graph()  # 获取当前图，为了后续训练时恢复变量
# tensor_name_list = [tensor.name for tensor in gragh.as_graph_def().node]  # 得到当前图中所有变量的名称

# meta_graph = tf.train.import_meta_graph('./model.ckpt.meta')  # 加载图结构
# gragh = tf.get_default_graph()  # 获取当前图，为了后续训练时恢复变量
# tensor_name_list = [tensor.name for tensor in gragh.as_graph_def().node]  # 得到当前图中所有变量的名称
# #print(tensor_name_list)
# with tf.Session() as sess:
#   meta_graph.restore(sess,'./model.ckpt')
# print(sess.run(tf.get_default_graph().get_tensor_by_name('conv1:0')))

# print(sess.run(tensor_name_list))

# graph = tf.get_default_graph()
# conv1_weights = graph.get_tensor_by_name("conv1_weights:0")
#
# print(sess.run(conv1_weights))
# w2 = graph.get_tensor_by_name("w2:0")
# feed_dict = {w1: 13.0, w2: 17.0}

# saver=tf.train.import_meta_graph('./model.ckpt.meta')

#
# model_path = './model.ckpt'
# reader = tf.train.NewCheckpointReader(model_path)
# all_variables = reader.get_variable_to_shape_map()
#
# # 分析 conv1 的权重
# conv1_weight = reader.get_tensor("conv1/weights")
# conv1_weight.shape
# #
# # 计算每个kernel权重的和 (也可以使用其他指标，如std，mean等)
# conv1_weight_sum = np.sum(conv1_weight, (0,1,2))
# sort_conv1_weights = np.sort(conv1_weight_sum)
#
# # 绘制conv1的
# x = np.arange(0,len(sort_conv1_weights),step=1)
# plt.plot(x,sort_conv1_weights)
#
# pure_conv1_weight_index = np.where(conv1_weight_sum >= sort_conv1_weights[8])
# pure_conv1_weight = conv1_weight[:,:,:,pure_conv1_weight_index[0]]
#
# # conv1对应的bias 也做相同处理
# conv1_bias = reader.get_tensor("conv1/biases")
# pure_conv1_bias = conv1_bias[pure_conv1_weight_index[0]]
# pure_conv1_bias
#
# conv2_weight = reader.get_tensor("conv2/weights")
# conv2_bias = reader.get_tensor("conv2/biases")
#
# conv2_weight = conv2_weight[:,:,pure_conv1_weight_index[0],:]
#
# # 同理 先计算每个kernel 的权重和 找到最无关的一些kernel
# conv2_weight_sum = np.sum(conv2_weight, (0,1,2))
# sort_conv2_weights = np.sort(conv2_weight_sum)
#
# # 绘制conv2的权重和分布图
# x = np.arange(0,len(sort_conv2_weights),step=1)
# plt.plot(x,sort_conv2_weights)
#
# pure_conv2_weight_index = np.where(conv2_weight_sum >= sort_conv2_weights[16])
# pure_conv2_weight = conv2_weight[:,:,:,pure_conv2_weight_index[0]]
# pure_conv2_weight.shape
#
# # conv2对应的bias 也做相同处理
# pure_conv2_bias = conv2_bias[pure_conv2_weight_index[0]]
# pure_conv2_bias

# conv3_weight = reader.get_tensor("conv3/weights")
# conv3_bias = reader.get_tensor("conv3/biases")
#
# conv3_weight = conv3_weight[:,:,pure_conv2_weight_index[0],:]
# conv3_weight.shape
# conv3_weight_sum = np.sum(conv3_weight, (0,1,2))
# sort_conv3_weights = np.sort(conv3_weight_sum)
#
# # 绘制conv3的权重和分布图
# x = np.arange(0,len(sort_conv3_weights),step=1)
# plt.plot(x,sort_conv3_weights)
# conv3_weight_std = np.std(conv3_weight, (0,1,2))
# sort_conv3_weights_std = np.sort(conv3_weight_std)
# # 绘制conv3的权重std分布图
# x = np.arange(0,len(sort_conv3_weights_std),step=1)
# plt.plot(x,sort_conv3_weights_std)
# pure_conv3_weight_index = np.where(conv3_weight_std >= sort_conv3_weights_std[8])
# pure_conv3_weight = conv3_weight[:,:,:,pure_conv3_weight_index[0]]
# pure_conv3_weight.shape
# # conv3对应的bias 也做相同处理
# pure_conv3_bias = conv3_bias[pure_conv3_weight_index[0]]
# pure_conv3_bias
#
#
# fc1_weight = reader.get_tensor("fc1/weights")
# fc1_bias = reader.get_tensor("fc1/biases")
# fc1_weight.shape
#
# # b h w c
# out['pool3'].get_shape()
# out_area = out['pool3'].get_shape()[1].value * out['pool3'].get_shape()[2].value
#
# pure_index = []
# for i in range(out_area):
#     pure_index += list(32 * i + pure_conv3_weight_index[0])
#
# # 获得每个kernel的权重和
# fc1_weight_sum = np.sum(fc1_weight, (0,))
# sort_fc1_weights = np.sort(fc1_weight_sum)
#
# # 绘制fc1的权重std分布图
# x = np.arange(0,len(sort_fc1_weights_std),step=1)
# plt.plot(x,sort_fc1_weights_std)
#
# pure_fc1_weight_index = np.where(fc1_weight_std >= sort_fc1_weights_std[96])
# pure_fc1_weight = fc1_weight[:,pure_fc1_weight_index[0]]
# pure_fc1_weight.shape
#
# # fc1 对应的bias 也做相同处理
# pure_fc1_bias = fc1_bias[pure_fc1_weight_index[0]]
# pure_fc1_bias
#
#
# fc2_weight = reader.get_tensor("fc2/weights")
# fc2_bias = reader.get_tensor("fc2/biases")
#
# fc2_weight.shape
#
# # 只删减kernel 的 通道， 对bias无影响
# fc2_weight = fc2_weight[pure_fc1_weight_index[0],:]
#
# # 获得每个kernel的权重和
# fc2_weight_sum = np.sum(fc2_weight, (0,))
# sort_fc2_weights = np.sort(fc2_weight_sum)
#
# # 绘制fc2的权重和分布图
# x = np.arange(0,len(sort_fc2_weights),step=1)
# plt.plot(x,sort_fc2_weights)
#
# # 获得每个kernel的std
# fc2_weight_std = np.std(fc2_weight, (0,))
# sort_fc2_weights_std = np.sort(fc2_weight_std)
#
#
# # 绘制fc1的权重std分布图
# x = np.arange(0,len(sort_fc2_weights_std),step=1)
# plt.plot(x,sort_fc2_weights_std)
#
# # 获得 logit 的权重
# logits_weight = reader.get_tensor("logits/weights")
# logits_bias = reader.get_tensor("logits/biases")
#
# channel_dict = {'conv1': pure_conv1_weight.shape[-1], 'conv2': pure_conv2_weight.shape[-1],
#                'conv3':pure_conv3_weight.shape[-1], 'fc1': pure_fc1_weight.shape[-1],
#                'fc2': fc2_weight.shape[-1], 'logits': logits_weight.shape[-1]}
#
# pure_weights = {'conv1/weights': pure_conv1_weight, 'conv1/biases': pure_conv1_bias,
#                'conv2/weights': pure_conv2_weight, 'conv2/biases': pure_conv2_bias,
#                'conv3/weights': pure_conv3_weight, 'conv3/biases': pure_conv3_bias,
#                'fc1/weights': pure_fc1_weight, 'fc1/biases': pure_fc1_bias,
#                'fc2/weights': fc2_weight, 'fc2/biases': fc2_bias,
#                'logits/weights': logits_weight, 'logits/biases': logits_bias}
#
# all_data = {}
# all_data['channel_dict'] = channel_dict
# all_data['pure_weights'] = pure_weights
#
# with open('./pure_checkpoints/pure_1.pb', 'wb') as f:
#     pickle.dump(all_data, f)
#
# with open('./pure_checkpoints/pure_1.pb', 'rb') as f:
# load = pickle.load(f)
#
# load['channel_dict']
#
# load['pure_weights']
