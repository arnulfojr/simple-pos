(fn => {
    'use strict'
    
    const productApp = angular.module('productApp', [])

    productApp.config(['$interpolateProvider', ($interpolateProvider) => {
        $interpolateProvider.startSymbol('[%')
        $interpolateProvider.endSymbol('%]')
    }])

    productApp.service('ProductApi', ['$http', '$q', function($http, $q) {

        this.getAll = () => {
            const url = '/api/products/'

            const context = {
                url: url,
                method: 'GET'
            }

            return $http(context)
        }

        this.get = (code) => {
            const url = `/api/products/${code}/`
            
            const context = {
                url: url,
                method: 'GET'
            }

            return $http(context)
        }

        this.add = (product) => {
            const url = '/api/products/'

            if (typeof product.price === 'string') {
                product.price = parseFloat(product.price)
            }

            const context = {
                url: url,
                method: 'POST',
                data: product
            }

            return $http(context)
        }

        this.update = (product) => {
            const url = `/api/products/${product.code}/`

            if (typeof product.price === 'string') {
                product.price = parseFloat(product.price)
            }

            const context = {
                url: url,
                method: 'PUT',
                data: product
            }

            return $http(context)
        }

    }])

    productApp.directive('productPanel', () => {
        return {
            restrict: 'E',
            scope: {
                product: '='
            },
            controller: ['$scope', ($scope) => {
                this.edit = (code) => {
                    window.location.href = `/products/edit/{code}/`
                }
            }],
            templateUrl: '/static/products/directives/panel.html'
        }
    })

    /**
     * Browse Controller
     */
    productApp.controller('BrowseController', ['$log', '$scope', 'ProductApi', ($log, $scope, ProductApi) => {
        $scope.products = []

        this.init = () => {
            ProductApi.getAll().then(
                response => {
                    $scope.products = response.data
                    console.log($scope.products)
                },
                error => {
                    console.error(error)
                }
            )
        }

        this.init()
    }])


    /**
     * Form Controller
     */
    productApp.controller('FormController', ['$scope', 'ProductApi', ($scope, ProductApi) => {
        $scope.product = {}
        $scope.isEdit = window.isEdit
        $scope.alert = {
            show: false,
            type: 'success',
            message: ""
        }

        this.init = () => {
            if ($scope.isEdit) {
                console.log('Form will edit a product', window.code)
                ProductApi.get(window.code).then(
                    response => {
                        $scope.product = response.data
                    },
                    error => {
                        console.error(error)
                    }
                )
            }

        }

        $scope.saveProduct = () => {
            $scope.alert.show = false

            let action = ($scope.isEdit) ? ProductApi.update : ProductApi.add

            action($scope.product).then(
                response => {
                    $scope.alert.show = true
                    $scope.alert.message = 'Request was successfully done!'
                    $scope.product = {}
                },
                error => {
                    console.error(error)
                    $scope.alert.show = true
                    $scope.alert.message = 'Error in the request'
                    
                    if (error.data) {
                        if (error.data.price !== undefined) {
                            $scope.alert.message = 'Price is a ' + error.data.price[0]
                        }
                    }

                    $scope.alert.type = 'danger'
                }
            )
        }

        this.init()
    }])

})();
