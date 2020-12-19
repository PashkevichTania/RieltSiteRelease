new Vue({
    el: '#emp',
    data: {
        employees:[]
    },
    created: function () {
        const vm = this;
        axios.get('/api/employees/')
        .then(function (response) {
            vm.employees = response.data
            console.log(response.data)
        })
    }
    }

)