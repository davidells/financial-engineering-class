from binomial_lattice import *

if __name__=='__main__':
    # From black scholes params
    model = convert_black_scholes_to_binomial_params(
        std_dev=0.3,
        interest_rate=0.02,
        time_to_maturity=0.25,
        dividend_yield=0.01,
        num_periods=15)

    model.update({
        "initial_value": 100,
        "option_type": 'put',
        "strike_price": 110
    })

    print
    for name in model:
        print "%s: %s" % (name, model[name])
    print


    sl_args = filter_dict(model, 
        ["up_move_change", "down_move_change",
         "initial_value", "num_periods"])

    sl = ValueChangeLattice(**sl_args)
    sl.display()


    opt_args = filter_dict(model,
        ["risk_free_probability", "gross_interest_rate",
         "option_type", "strike_price"])

    opt_args.update({
        "underlying_lattice": sl
    })

    opt = OptionPriceLattice(**opt_args)
    opt.display()


    fut = FuturesPriceLattice(
            risk_free_probability=model["risk_free_probability"],
            underlying_lattice=sl)
    fut.display()

    opt2_args = opt_args.copy()
    opt2_args.update({
        "underlying_lattice": fut,
        "option_type": "call",
        "strike_price": 110,
        "expiration": 10
    })

    opt2 = OptionPriceLattice(**opt2_args)
    opt2.display()

    
    chooser_call_args = opt_args.copy()
    chooser_call_args.update({
        "option_type": "call",
        "option_style": "european",
        "strike_price": 100
    })
    chooser_call_opt = OptionPriceLattice(**chooser_call_args)
    print "\nChooser call option\n"
    chooser_call_opt.display()

    chooser_put_args = chooser_call_args.copy()
    chooser_put_args["option_type"] = "put"
    chooser_put_opt = OptionPriceLattice(**chooser_put_args)
    print "\nChooser put option\n"
    chooser_put_opt.display()


    combo_option_mtx = max_matrices(
        chooser_call_opt.compute(),
        chooser_put_opt.compute())

    chooser_expiration = 10
    for i in range(chooser_expiration):
        for j in range(i+1):
            combo_option_mtx[i][j] = 0

    combo_opt_lat = StaticLattice(
        underlying_matrix=combo_option_mtx)

    print '\nCombined prices\n'
    combo_opt_lat.display()

    chooser_opt_args = opt_args.copy()
    chooser_opt_args.update({
        "underlying_lattice": combo_opt_lat,
        "option_style": "european",
        "option_type": "call",
        "strike_price": 0,
        "expiration": 10
    })
    chooser_opt = OptionPriceLattice(**chooser_opt_args)
    print '\nChooser Option\n'
    chooser_opt.display()

    #P0 = 12.36
    #S0 = 100
    #c = 0.01
    #T = 0.25
    #C0 = 2.6
    #K = 110
    #r = 0.02
    #print P0 + S0 * math.exp(-c * T)
    #print C0 + K * math.exp(-r * T)







    sl1 = ValueChangeLattice(
            up_move_change=1.07,
            down_move_change=0.93458,
            initial_value=100,
            num_periods=3)

    opt1 = OptionPriceLattice(
            risk_free_probability=0.5570,
            gross_interest_rate=1.01,
            option_type='put',
            strike_price=100,
            underlying_lattice=sl1)

    #sl1.display()
    #opt1.display()

    gross_rate = math.exp((0.02*0.5)/10)

    sl2 = ValueChangeLattice(
            up_move_change=1.04574,
            down_move_change=0.95626,
            initial_value=100,
            num_periods=10)

    fut2 = FuturesPriceLattice(
            risk_free_probability=0.4944,
            underlying_lattice=sl2)
    
    opt2 = OptionPriceLattice(
            risk_free_probability=0.4944,
            gross_interest_rate=gross_rate,
            option_style='european',
            option_type='put',
            strike_price=100,
            #expiration=9,
            underlying_lattice=fut2)

    st2 = StaticLattice(
            underlying_matrix=opt2.compute())

    #sl2.display()
    #fut2.display()
    #opt2.display()
    #st2.display()
        
    mtx = add_matrices(opt2.compute(), st2.compute())
    st2a = StaticLattice(underlying_matrix=mtx)
    #st2a.display()



