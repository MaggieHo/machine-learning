## install git
class install_modules {
    include git
    include stdlib
}

## create '/vagrant/build/' directory
include system::build_directory

## install sklearn dependencies
include package::sklearn_dependencies

## download scikit-learn
include package::sklearn

## build scikit-learn
include sklearn::build_sklearn

## install scikit-learn
include sklearn::install_sklearn