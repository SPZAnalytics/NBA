library(caret)
library(caretEnsemble)
library(doMC)
registerDoMC(cores = 2)

set.seed(107)
preprocessParams <- preProcess(dataset, method=c("center", "scale", "pca"))
transformed <- predict(preprocessParams, dataset)
inTrain <- createDataPartition(y = transformed$gtproj, p = .75, list = FALSE)
training = transformed[inTrain,]
testing = transformed[-inTrain,]

algorithmList <- c('gbm', 'rpart', 'knn', 'svmRadial', 'xgbLinear', 'rf', 'treebag')
my_control <- trainControl(
  method="boot",
  number=25,
  savePredictions="final",
  classProbs=TRUE,
  index=createResample(training$gtproj, 25),
  summaryFunction=twoClassSummary
)
model_list <- caretList(gtproj~., data=training, metric="Accuracy", trControl=my_control, methodList=algorithmList, verbose = FALSE)

greedy_ensemble <- caretEnsemble(
  model_list, 
  metric="ROC",
  trControl=trainControl(
    number=2,
    summaryFunction=twoClassSummary,
    classProbs=TRUE
  ))
summary(greedy_ensemble)

model_preds <- lapply(model_list, predict, newdata=testing, type="prob")
model_preds <- lapply(model_preds, function(x) x[,"gt"])
model_preds <- data.frame(model_preds)
ens_preds <- predict(greedy_ensemble, newdata=testing, type="prob")
model_preds$ensemble <- ens_preds
caTools::colAUC(model_preds, testing$gtproj)

# glm_ensemble <- caretStack(
#   model_list,
#   method="glm",
#   metric="ROC",
#   trControl=trainControl(
#     method="boot",
#     number=10,
#     savePredictions="final",
#     classProbs=TRUE,
#     summaryFunction=twoClassSummary
#   )
# )
# 
# model_preds2 <- model_preds
# model_preds2$ensemble <- predict(glm_ensemble, newdata=testing, type="prob")
# CF <- coef(glm_ensemble$ens_model$finalModel)[-1]
# colAUC(model_preds2, testing$gtproj)

gbm_ensemble <- caretStack(
  model_list,
  method="gbm",
  verbose=FALSE,
  tuneLength=10,
  metric="ROC",
  trControl=trainControl(
    method="boot",
    number=10,
    savePredictions="final",
    classProbs=TRUE,
    summaryFunction=twoClassSummary
  )
)
model_preds3 <- model_preds
model_preds3$ensemble <- predict(gbm_ensemble, newdata=testing, type="prob")
colAUC(model_preds3, testing$gtproj)

