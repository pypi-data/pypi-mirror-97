from loguru import logger
import torch

class ModelInformationNotFoundException(Exception):
    pass

class ModelToolbox:
    def __init__(self, model_class, optimizer_class):
        self.model_class = model_class
        self.optimizer_class = optimizer_class


    def save_model(self, miner_path, model_info):
        """Saves the model locally. 

        Args:
            model_info (:obj:`dict`, `required`): Dictionary containing the epoch we are saving at, the loss, and the PyTorch model object.

        Raises:
            :obj:`ModelInformationNotFoundException`: Raised whenever the loss, epoch, or PyTorch model object is missing from the input dictionary.
        """
        try:
            if 'epoch' not in model_info.keys():
                raise ModelInformationNotFoundException("Missing 'epoch' in torch save dict")

            if 'loss' not in model_info.keys():
                raise ModelInformationNotFoundException("Missing 'loss' in torch save dict")
            
            if 'model_state_dict' not in model_info.keys():
                raise ModelInformationNotFoundException("Missing 'model' in torch save dict")

            if 'optimizer_state_dict' not in model_info.keys():
                raise ModelInformationNotFoundException("Missing 'optimizer' in torch save dict")
            
            logger.info( 'Saving/Serving model: epoch: {}, loss: {}, path: {}/model.torch'.format(model_info['epoch'], model_info['loss'], miner_path))
            torch.save(model_info,"{}/model.torch".format(miner_path))

        except ModelInformationNotFoundException as e:
            logger.error("Encountered exception trying to save model: {}", e)
    
    def load_model(self, config):
        """ Loads a model saved by save_model() and returns it. 

        Returns:
           model (:obj:`torch.nn.Module`) : Model that was saved earlier, loaded back up using the state dict and optimizer. 
           optimizer (:obj:`torch.optim`) : Model optimizer that was saved with the model.
        """
        model = self.model_class( config )
        optimizer = self.optimizer_class(model.parameters(), lr = config.miner.learning_rate, momentum=config.miner.momentum)
        
        try:
            checkpoint = torch.load("{}/model.torch".format(config.miner.full_path))
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            epoch = checkpoint['epoch']
            loss = checkpoint['loss']

            logger.info( 'Reloaded model: epoch: {}, loss: {}, path: {}/model.torch'.format(epoch, loss, config.miner.full_path))
        except Exception as e:
            logger.warning ( 'Exception {}. Could not find model in path: {}/model.torch', e, config.miner.full_path )


        return model, optimizer


