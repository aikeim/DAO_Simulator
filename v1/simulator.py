import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from skopt import Optimizer
from skopt.space import Real
from dao2 import DAO

def objective_function(params):
    token_incentive, nft_incentive, token_price, nft_price = params
    dao = DAO(token_incentive, nft_incentive, token_price, nft_price)
    score = dao.simulate_communication_activation()
    return -score  # 最大化問題に変換するために符号を反転させる

def run_optimization():
    space = [Real(5, 20, name='token_incentive'),
            Real(2, 10, name='nft_incentive'),
            Real(30, 70, name='token_price'),
            Real(100, 300, name='nft_price')]

    optimizer = Optimizer(space, base_estimator="GP", n_initial_points=10, acq_func="EI")

    for _ in range(50):
        params = optimizer.ask()
        score = objective_function(params)
        optimizer.tell(params, score)

    return optimizer

def prepare_data(optimizer):
    data = pd.DataFrame(optimizer.Xi, columns=['Token Incentive', 'NFT Incentive', 'Token Price', 'NFT Price'])
    data['Score'] = -np.array(optimizer.yi)  # 符号を元に戻す
    return data

def plot_heatmap(data, x_label, y_label, title):
    # ヒートマップ用のデータを整形
    heatmap_data = data.pivot_table(index=y_label, columns=x_label, values='Score', aggfunc='mean')

    # グラフのサイズを調整
    plt.figure(figsize=(12, 8))
    
    # ヒートマップのプロット設定
    ax = sns.heatmap(heatmap_data, annot=True, fmt=".2f", linewidths=.5, cmap='coolwarm',
                    annot_kws={'fontsize': 10, 'color': 'black'},
                    cbar_kws={'label': 'Communication Activation Score'})

    # 軸のティックラベルの間隔を調整
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_yticks(ax.get_yticks()[::2])

    # ラベルを小数点2桁にする
    x_labels = ['{:.2f}'.format(label) for label in ax.get_xticks()]
    y_labels = ['{:.2f}'.format(label) for label in ax.get_yticks()]

    # 軸のティックラベルを設定
    ax.set_xticklabels(x_labels, fontsize=10)
    ax.set_yticklabels(y_labels, fontsize=10)
    
    # タイトルとラベルを設定
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show()

def plot_scatter(data, x_label, y_label, title):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x=x_label, y=y_label, hue='Score', size='Score', sizes=(20, 200), palette='coolwarm')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def plot_3d_scatter(data, x_label, y_label, z_label, title):
    fig = px.scatter_3d(data, x=x_label, y=y_label, z=z_label, color='Score', size='Score', color_continuous_scale='Viridis')
    fig.update_layout(title=title, scene=dict(xaxis_title=x_label, yaxis_title=y_label, zaxis_title=z_label))
    fig.show()

def main():
    optimizer = run_optimization()
    data = prepare_data(optimizer)

    # ヒートマップをプロット
    plot_heatmap(data, 'Token Price', 'NFT Price', 'Communication Activation Heatmap')

    # 散布図をプロット
    plot_scatter(data, 'Token Price', 'NFT Price', 'Scatter Plot of Simulation Results')

    # 3次元散布図をプロット
    plot_3d_scatter(data, 'Token Price', 'NFT Price', 'Score', '3D Scatter Plot of Simulation Results')

if __name__ == "__main__":
    main()