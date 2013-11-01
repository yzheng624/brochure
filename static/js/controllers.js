var app = angular.module('brochureApp', ['ngResource']);

app.factory('productFactory', ['$http', function ($http) {
    var urlBase = '/';
    var productFactory = {};

    productFactory.query = function (url) {
        data = {'url': url};
        return $http.post(urlBase + 'query_bestbuy/', data);
    };

    productFactory.getCustomer = function (id) {
        return $http.get(urlBase + '/' + id);
    };

    productFactory.insertCustomer = function (cust) {
        return $http.post(urlBase, cust);
    };

    productFactory.updateCustomer = function (cust) {
        return $http.put(urlBase + '/' + cust.ID, cust)
    };

    productFactory.deleteCustomer = function (id) {
        return $http.delete(urlBase + '/' + id);
    };

    productFactory.getOrders = function (id) {
        return $http.get(urlBase + '/' + id + '/orders');
    };

    return productFactory;
}]);

app.controller('brochureController', ['$scope', 'productFactory', function ($scope, productFactory) {
    $scope.products = [{first: 'Yan', last: 'Zheng', username: 'yanzheng'}, {first: 'Yan', last: 'Zheng', username: 'yanzheng'}, {first: 'Yan', last: 'Zheng', username: 'yanzheng'}, {first: 'Yan', last: 'Zheng', username: 'yanzheng'}];
    $scope.bestBuyClicked = function () {
        $scope.products = [{first: 'Xhacker', last: 'Liu', username: 'xhacker'}];
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
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.query($scope.queryUrl).success(function (product) {
            $scope.spinner.stop();
            $scope.productDetail = product;
            $('#addLinkNext').hide();
            $('#addLinkDetail').show();
        });
    };
}]);