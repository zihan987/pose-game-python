import torch 

# 姿态分类器
class PoseClassification(torch.nn.Module):

    # 初始化
    def __init__(self, x_features, num_moves):      # x_features: 图片特征数量，num_moves: 动作数量
        super(PoseClassification, self).__init__()  # 继承父类
        self.model = torch.nn.Sequential(           # 创建网络
           
            # 卷积层（1）
            torch.nn.Linear(x_features, 500),       # 线性层
            torch.nn.BatchNorm1d(500),              # 批归一化层
            torch.nn.ReLU(),                        # 激活层
            torch.nn.Dropout(p=0.2),                # Dropout层

            # 卷积层（2）
            torch.nn.Linear(500,1000),              # 线性层
            torch.nn.BatchNorm1d(1000),             # 批归一化层
            torch.nn.ReLU(),                        # 激活层
            torch.nn.Dropout(p=0.2),                # Dropout层

            # 卷积层（3）
            torch.nn.Linear(1000,1000),             # 线性层
            torch.nn.BatchNorm1d(1000),             # 批归一化层
            torch.nn.ReLU(),                        # 激活层
            torch.nn.Dropout(p=0.2),                # Dropout层

            # 卷积层（4）
            torch.nn.Linear(1000,500),              # 线性层
            torch.nn.BatchNorm1d(500),              # 批归一化层
            torch.nn.ReLU(),                        # 激活层
            torch.nn.Dropout(p=0.2),                # Dropout层

            # 卷积层（5）
            torch.nn.Linear(500,200),               # 线性层
            torch.nn.BatchNorm1d(200),              # 批归一化层
            torch.nn.ReLU(),                        # 激活层
            torch.nn.Dropout(p=0.2),                # Dropout层

            # 卷积层（6）
            torch.nn.Linear(200,50),                # 线性层
            torch.nn.BatchNorm1d(50),               # 批归一化层
            torch.nn.ReLU(),                        # 激活层
            torch.nn.Dropout(p=0.2),                # Dropout层

            # 卷积层（7）
            torch.nn.Linear(50,num_moves),          # 线性层
        )
    
    # 加载模型
    def forward(self,x):
        return self.model(x)

# 姿态分类器测试
def test():

    # 模型初始化（图片特征数量60，动作数量4）
    model = PoseClassification(60,4)
    # 模型加载
    x = torch.randn((5,60))
    
    # 模型输出
    output = model(x)
    
    # 打印模型输出维度
    print(f'Input shape : {x.shape}, Output shape : {output.shape}')