(fn => {
    'use strict'

    const app = angular.module('cashierApp', [])

    app.config(['$interpolateProvider', ($interpolateProvider) => {
        $interpolateProvider.startSymbol('[%')
        $interpolateProvider.endSymbol('%]')
    }])

    app.service('ProductApi', ['$http', function($http) {
        this.getAll = () => {
            const url = '/api/products/'

            const context = {
                method: 'GET',
                url: url
            }

            return $http(context)
        }
    }])

    app.service('TransactionApi', ['$http', function($http) {
        this.save = (order) => {
            const url = '/api/transactions/'

            const context = {
                method: 'POST',
                url: url,
                data: order
            }

            return $http(context)
        }

        this.getAll = (params) => {
            const url = '/api/transactions/'
            const context = {
                url: url,
                method: 'GET'
            }

            if (params !== undefined) {
                context.params = params
            }

            return $http(context)
        }

        this.deliver = (transaction) => {
            const url = `/api/transactions/${transaction.code}/deliver/`

            const context = {
                url: url,
                method: 'PUT'
            }

            return $http(context)
        }

    }])

    app.service('Order', function() {
        this.order = {
            delivered: false,
            items: []
        }

        this.total = 0

        this.delivered = false

        this.getTotal = () => {
            let total = 0

            angular.forEach(this.order.items, (item) => {
                total += item.product.price * item.quantity
            })

            return total
        }

        this.empty = () => {
            this.order.items = []
            this.total = this.getTotal()
        }

        this.items = () => {
            return this.order.items
        }

        this.add = (product) => {
            let exists = false

            angular.forEach(this.order.items, (item) => {
                if (item.product && item.product.code === product.code) {
                    exists = true
                    item.quantity++
                }
            })

            if (!exists) {
                let item = {
                    quantity: 1,
                    product: product
                }
                this.order.items.push(item)
            }

            this.total = this.getTotal()
        }

        this.remove = (itemToRemove) => {
            let exists = false
            let remove = false

            angular.forEach(this.order.items, (item) => {
                if (item.product.code === itemToRemove.product.code) {
                    exists = true
                    remove = item.quantity === 1
                    if (!remove) {
                        item.quantity--
                    }
                }
            })

            if (exists && remove) {
                const index = this.order.items.indexOf(itemToRemove)
                if (index !== -1) {
                    this.order.items.splice(index, 1)
                }
            }

            this.total = this.getTotal()
        }
    })

    app.controller('CashierController', ['$scope', 'TransactionApi', 'Order', ($scope, transApi, Order) => {
        $scope.order = Order
        $scope.alert = {
            show: false,
            message: '',
            type: ''
        }

        $scope.empty = () => {
            Order.empty()
            $scope.income = 0
        }

        $scope.addOrder = () => {
            $scope.order.delivered = false
            $scope.alert.show = false
            $scope.alert.message = ''
            transApi.save($scope.order.order)
                .then(response => {
                    $scope.alert.show = true
                    $scope.alert.type = 'alert-info'
                    $scope.alert.message = 'Sent the order, ready to new order'
                    $scope.empty()
                }, error => {
                    $scope.alert.show = true
                    $scope.alert.type = 'alert-danger'
                    $scope.alert.message = 'Error sending the order'
                })
        }

        $scope.remove = (item) => {
            Order.remove(item)
        }
    }])

    app.controller('ProductController', ['$scope', 'ProductApi', 'Order', ($scope, prodApi, Order) => {

        $scope.products = []

        this.init = () => {
            prodApi.getAll()
                .then(response => {
                    $scope.products = response.data
                    console.log(response.data)
                })
        }

        $scope.add = (product) => {
            Order.add(product)
        }

        this.init()
    }])

    app.controller('OrderController', ['$scope', '$interval', 'TransactionApi', ($scope, $interval, tApi) => {
        $scope.transactions = []

        $scope.deliver = (transaction) => {
            tApi.deliver(transaction).then(response => {
                $scope.refresh()
            })
        }

        $scope.refresh = () => {
            tApi.getAll({delivered: false}).then(response => {
                $scope.transactions = response.data
            })
        }

        this.init = () => {
            $interval(() => { $scope.refresh() }, 2500)
        }

        this.init()

    }])
})()
