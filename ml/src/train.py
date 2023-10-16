import argparse
import yaml
from io import StringIO
import pandas as pd





# def main():
    # params = load_params(args.params)
    
    # project_dir = f"{params['project']}/{params['target']}"
    # data_dir = f"{params['data_dir']}/{params['target']}"
    # model_dir = f"{params['project']}/{params['target']}/{params['model_dir']}"
    # print(data_dir)
    # print(model_dir)
    
    # train(
    #     project_dir=project_dir,
    #     processed_data=data_dir, 
    #     model_dir=model_dir, 
    #     model_type=args.type, 
    #     target=args.target
    # )


def train(project_dir: str, processed_data: str, model_dir: str, model_type: str, target: str, epochs: int = 10):
    model = StringIO()
    df = pd.read_csv(f'{processed_data}/processed/data.csv', header=None)
    for _, row in df.iterrows():
        for cell in row:
            model.write(cell)
            
    model_path = f'{model_dir}/model_{model_type}_{target}.file' 
    print(model_path)
    
    with open(model_path, 'w') as f:
        f.write(model.getvalue())
        
    # Generate Metrics 
    import random
    from dvclive import Live
    
    if model_type == 'pipeline_a_segment':
        with Live(
            dir=f"{project_dir}/dvclive", 
            save_dvc_exp=False,
            dvcyaml=True,
            ) as live:
            
            choices = [i for i in range(95-epochs*2, 95-epochs)]
            randomlist = random.sample(choices, epochs)  
            
            for i,n in enumerate(randomlist):
                live.log_metric("accuracy", i + n )
                live.next_step()
    else: 
        with Live(
            dir=f"{project_dir}/results", 
            save_dvc_exp=False,
            dvcyaml=False,
            ) as live:
            
            choices = [i for i in range(95-epochs*2, 95-epochs)]
            randomlist = random.sample(choices, epochs)  
            
            for i,n in enumerate(randomlist):
                live.log_metric("accuracy", i + n )
                live.next_step()
    


def load_params(filename: str):
    with open(filename, 'r') as f:
        params = yaml.safe_load(f)
        return params 


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', help='model type')
    parser.add_argument('--target', help='target of data')
    parser.add_argument('--params', help='path to params.yaml')
    args = parser.parse_args()
    
    
    params = load_params(args.params)
    project_dir = f"{params['project']}/{params['target']}"
    data_dir = f"{params['data_dir']}/{params['target']}"
    model_dir = f"{params['project']}/{params['target']}/{params['model_dir']}"
    print(project_dir)
    # print(data_dir)
    # print(model_dir)
    
    train(
        project_dir=project_dir,
        processed_data=data_dir, 
        model_dir=model_dir, 
        model_type=args.type, 
        target=args.target,
        epochs=params['train']['epochs']
    )
