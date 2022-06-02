import torch 

class PoseClassification(torch.nn.Module):

    def __init__(self, x_features, num_moves):
        super(PoseClassification, self).__init__()
        self.model = torch.nn.Sequential(
            torch.nn.Linear(x_features, 500),
            torch.nn.BatchNorm1d(500), 
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),

            torch.nn.Linear(500,1000),
            torch.nn.BatchNorm1d(1000),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),

            torch.nn.Linear(1000,1000),
            torch.nn.BatchNorm1d(1000),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),

            torch.nn.Linear(1000,500),
            torch.nn.BatchNorm1d(500),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),

            torch.nn.Linear(500,200),
            torch.nn.BatchNorm1d(200),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),

            torch.nn.Linear(200,50),
            torch.nn.BatchNorm1d(50),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.2),

            torch.nn.Linear(50,num_moves),
        )
    
    def forward(self,x):
        return self.model(x)

def test():
    model = PoseClassification(60,4)
    x = torch.randn((5,60))
    output = model(x)
    print(f'Input shape : {x.shape}, Output shape : {output.shape}')