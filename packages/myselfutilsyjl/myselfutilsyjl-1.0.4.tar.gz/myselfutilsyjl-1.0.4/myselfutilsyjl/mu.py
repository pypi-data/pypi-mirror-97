# 本次更新内容：
# version：1.0.4
# 1、在draw_confusion_mat()函数中加入了try-except AttributeError，因为model.predict_classes()使用api创建模型时可能没有该函数

# version:1.0.3
# 1、help（）函数中加入      print('#de_to_one_hot_auto(labels)')
# 2、draw_result()函数中如果savepath=None，则不保存，只绘制


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
import random


def help():
    print('#draw_result(history, savepath)')
    print('#draw_confusion_mat(model, test_features, test_labels, classes, savepath)')
    print('#to_one_hot(labels, dimension=2, begin=1)')
    print('#de_to_one_hot_3dim(labels)')
    print('#de_to_one_hot(labels)')
    print('#de_to_one_hot_auto(labels)')
    print('#random_split(all_num, train_ratio, validation_ratio, test_ratio)')


# 绘制loss以及acc的图
def draw_result(history, savepath=None):
    acc = history['acc']
    val_acc = history['val_acc']
    loss = history['loss']
    val_loss = history['val_loss']

    epochs = range(1, len(acc) + 1)
    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.plot(epochs, acc, 'b', label='Training acc')
    plt.plot(epochs, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    if savepath is not None:
        plt.savefig(savepath + 'acc.jpg', dpi=200, bbox_inches='tight')

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    if savepath is not None:
        plt.savefig(savepath + 'loss.jpg', dpi=200, bbox_inches='tight')

    plt.show()


# 绘制混淆矩阵(用归一化之后的数据绘图)
# 此处的plt.cm.Blues的具体颜色映射参考网址：https://matplotlib.org/gallery/color/colormap_reference.html
def plot_confusion_matrix(cm, classes, title, savepath, normalize=False, cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    # plt.xticks(tick_marks, classes, rotation=45)
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    plt.tick_params(axis='both', which='both', bottom=False, left=False)
    # plt.tick_params(axis='y', which='both', bottom=False)

    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, '{:>.4f}'.format(cm[i, j]), horizontalalignment='center',
                 color='white' if cm[i, j] > thresh else 'black')

    # plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predict label')
    plt.savefig(savepath + '混淆矩阵.jpg', dpi=200, bbox_inches='tight')
    plt.show()


# 整理绘制混淆矩阵所需的数据
def draw_confusion_mat(model, test_features, test_labels, classes, savepath):
    try:
        test_labels_predict = model.predict_classes(test_features)  # shape(1094,20)
    except AttributeError:
        temp_test_predict = model.predict(test_features)
        test_labels_predict = np.argmax(temp_test_predict, axis=-1)  # shape(1094,20)
    test_labels_predict = test_labels_predict.reshape((-1, 1)).astype(np.int32)  # shape(21800,1)int型,范围为(0-4)
    test_labels_true = de_to_one_hot_auto(test_labels).reshape((-1, 1)).astype(np.int32)  # shape(21800,1)int型,范围为(0-4)

    # 画混淆矩阵
    confusion_mat = confusion_matrix(test_labels_true, test_labels_predict)
    # self.plot_confusion_matrix(confusion_mat, classes=range(5), title=f'Confusion matrix {class_dict}', normalize=True)
    plot_confusion_matrix(confusion_mat, classes, savepath=savepath, title=f'Confusion matrix', normalize=True)


# 将样本转为one_hot形式，labels为（seample，1）或（seample,),dimension默认为2，也就是转成one_hot之后会有几列（几类）
# begin为labels中开始的下表，例如，labels：（1,2,3,1,3,2,1,2）其中为3分类的话dimension为3，而begin为1.
def to_one_hot(labels, dimension=2, begin=1):
    results = np.zeros((len(labels), dimension))
    for i, label in enumerate(labels):
        results[i, label - begin] = 1
    return results


# 将one_hot形式转化为非one_hot的形式，也即是从（seample,5)转化为(seample)此处的函数为处理三维转二维的，
# 也即是（seample/20,20,5)转化为（seample/20,20)
def de_to_one_hot_3dim(labels):
    if len(labels.shape) != 3:
        print('de_to_one_hot_3dim此方法仅适用于三维转二维')
        exit()
    results = np.zeros((labels.shape[:-1]))
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            results[i][j] = np.argwhere(labels[i][j] == 1).ravel()[0]
    return results


# 将one_hot形式转化为非one_hot的形式，也即是从（seample,5)转化为(seample)，
def de_to_one_hot(labels):
    if len(labels.shape) != 2:
        print('de_to_one_hot此方法仅适用于二维转一维')
        exit()
    results = np.zeros((labels.shape[0],))
    for i in range(labels.shape[0]):
        results[i] = np.argwhere(labels[i] == 1).ravel()[0]
    return results


# 可以支持三维转二维的或者二维转一维的
def de_to_one_hot_auto(labels):
    if len(labels.shape) == 2:
        return de_to_one_hot(labels)
    elif len(labels.shape) == 3:
        return de_to_one_hot_3dim(labels)
    else:
        print("目前仅支持三维转二维或者二维转一维!")
        exit()



# 做随机分割样本，all_num为样本总数，train_ratio为要分出训练集的比例，例如（124000,7,2,1）
# 返回值分别为训练集，测试集，验证集在all_num这样一个列表中的下表值
# 比如:(10,6,2,2)——>[2,5,6,8,1,9],[4,3],[7,0]
def random_split(all_num, train_ratio, validation_ratio, test_ratio):
    if train_ratio + validation_ratio + test_ratio != 10:
        print("请输入正确的比例，比例之和为10")
        exit()
    temp = list(range(all_num))
    random.shuffle(temp)
    return temp[:int(train_ratio / 10 * all_num)], temp[int(train_ratio / 10 * all_num):int(
        (train_ratio + validation_ratio) / 10 * all_num)], temp[int(-test_ratio / 10 * all_num):]
