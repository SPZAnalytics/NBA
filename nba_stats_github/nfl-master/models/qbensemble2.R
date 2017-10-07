library(caret)
library(caretEnsemble)

dfr = read.csv('qbmodel.csv')
dfr = dfr[dfr$AvgPts >= 12,]
set.seed(13)
preprocessParams <- preProcess(dfr, method=c("center", "scale"))
print(preprocessParams)
transformed <- predict(preprocessParams, dfr)
inTrain <- createDataPartition(y = transformed$ActualPoints, p = .75, list = FALSE)
training = transformed[inTrain,]
testing = transformed[-inTrain,]
std = preprocessParams$std['ActualPoints']
avg = preprocessParams$mean['ActualPoints']

#algorithmList <- c('glmStepAIC', 'lasso', 'bagEarth', 'glmboost', 'gbm', 'knn', 'brnn', 'rf')
algorithmList <- c('lm', 'lasso', 'glmboost', 'rf', 'knn', 'brnn')

rmse <- function(error) {sqrt(mean(error^2))}

models <- function(training.data, label, algorithm_list) {
  # returns list of caret models
  caretList(x=training.data[,1:ncol(training.data)-1], 
            y=training.data[,ncol(training.data)], 
            trControl=trainControl(
              method="boot",
              number=25,
              savePredictions="final",
              classProbs=FALSE,
              index=createResample(training.data[[label]], 25),
              summaryFunction=defaultSummary
            ), 
            methodList=algorithm_list)
}

modelCor(resamples(model_list))

# GREEDY ENSEMBLE
greedyEnsemble <- function(model_list, testing.data){
  ge = caretEnsemble(
    model_list,
    trControl=trainControl(
      number=5, repeats = 3,
      summaryFunction=defaultSummary
    )
  )
  model_preds <- lapply(model_list, predict, newdata=testing.data)
  model_preds <- data.frame(model_preds)
  ens_preds <- predict(ge, newdata=testing.data)
  model_preds$ensemble <- ens_preds
  model_preds  
}
  
rmse((testing$ActualPoints * std + avg) - (model_preds$ensemble * std + avg))

# GLM ENSEMBLE
glmEnsemble <- function(model_list, testing.data) {
  glm_ensemble <- caretStack(
    model_list,
    method="glm",
    metric="RMSE",
    trControl=trainControl(
      method="boot",
      number=10,
      savePredictions="final",
      summaryFunction=defaultSummary
    )
  )

  model_preds <- lapply(model_list, predict, newdata=testing.data)
  model_preds <- data.frame(model_preds)
  ens_preds <- predict(glm_ensemble, newdata=testing.data)
  model_preds$ensemble <- ens_preds
  model_preds  
}

# GBM ENSEMBLE
gbmEnsemble <- function(model_list, testing.data) {
  gbm_ensemble <- caretStack(
    model_list,
    method="gbm",
    verbose=FALSE,
    tuneLength=10,
    metric="RMSE",
    trControl=trainControl(
      method="boot",
      number=10,
      savePredictions="final",
      summaryFunction=defaultSummary
    )
  )
  model_preds <- lapply(model_list, predict, newdata=testing.data)
  model_preds <- data.frame(model_preds)
  ens_preds <- predict(gbm_ensemble, newdata=testing.data)
  model_preds$ensemble <- ens_preds
  model_preds  
}

#summary(gbm_ensemble)
#rmse((testing$ActualPoints * std + avg) - (model_preds3$ensemble * std + avg))