var app = angular.module('brochureApp', ['ngResource']);

app.factory('productFactory', ['$http', function ($http) {
    var urlBase = '/';
    var productFactory = {};

    productFactory.query = function (url) {
        data = {'url': url};
        return $http.post(urlBase + 'query_bestbuy/', data);
    };

    productFactory.addWatchlist = function (data) {
        return $http.post(urlBase + 'add_watchlist/', data);
    };

    productFactory.getAll = function () {
        return $http.get(urlBase + 'get_bestbuy/');
    };

    productFactory.getWatchlist = function () {
        return $http.get(urlBase + 'get_watchlist/');
    };

    return productFactory;
}]);

app.controller('brochureController', ['$scope', 'productFactory', function ($scope, productFactory) {
    var opts = {
            lines : 13, // The number of lines to draw
            length : 7, // The length of each line
            width : 4, // The line thickness
            radius : 10, // The radius of the inner circle
            corners : 1, // Corner roundness (0..1)
            rotate : 0, // The rotation offset
            color : '#000', // #rgb or #rrggbb
            speed : 1, // Rounds per second
            trail : 60, // Afterglow percentage
            shadow : false, // Whether to render a shadow
            hwaccel : false, // Whether to use hardware acceleration
            className : 'spinner', // The CSS class to assign to the spinner
            zIndex : 2e9, // The z-index (defaults to 2000000000)
            top : $(window).height()/2.5, // Manual positioning in viewport
            left : "auto"
        };
    $scope.bestBuyClicked = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.getAll().success(function (products) {
            productFactory.getWatchlist().success(function (watchlist) {
                for (var i = 0; i < products.length; i++) {
                    for (var j = 0; j < watchlist.length; j++) {
                        if (products[i].pk === watchlist[j].fields.product) {
                            products[i].fields.desire_price = watchlist[j].fields.desire_price;
                        }
                    }
                }
            });
            $scope.spinner.stop();
            $scope.products = products;
        });
        $('#bestBuyList').addClass('active');
        $('#welcome').hide();
        $('#menubar').show();
        $('#hr').show();
        $('#table').show();
    };
    $scope.addLink = function () {
        $('#menubar').hide();
        $('#hr').hide();
        $('#table').hide();
        $('#addLink').show();
        $('#addLinkNext').show();
        $('#addLinkDetail').hide();
    };
    $scope.addLinkNext = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.query($scope.new.queryUrl).success(function (product) {
            $scope.spinner.stop();
            url = $scope.new.queryUrl;
            $scope.new = product;
            $scope.new.queryUrl = url;
            $('#addLinkNext').hide();
            $('#addLinkDetail').show();
        });
    };
    $scope.submitProduct = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'url': $scope.new.queryUrl,
            'desire_price': $scope.new.desire_price,
            'current_price': $scope.new.current_price,
            'original_price': $scope.new.original_price,
            'name': $scope.new.name,
            'email': $scope.new.email
        };
        productFactory.addWatchlist(data).success(function (info) {
            productFactory.getAll().success(function (products) {
                productFactory.getWatchlist().success(function (watchlist) {
                    for (var i = 0; i < products.length; i++) {
                        for (var j = 0; j < watchlist.length; j++) {
                            if (products[i].pk === watchlist[j].fields.product) {
                                products[i].fields.desire_price = watchlist[j].fields.desire_price;
                            }
                        }
                    }
                });
                $scope.spinner.stop();
                $scope.products = products;
                $scope.spinner.stop();
            });
            $('#addLink').hide();
            $('#addLinkNext').hide();
            $('#addLinkDetail').show();
            $('#menubar').show();
            $('#hr').show();
            $('#table').show();
        });
    };
}]);