import binomial_lattice as bl

if __name__=='__main__':
    # From spreadsheet examples - ZCB+Options
    short_rate = bl.ValueChangeLattice(
        initial_value=0.06,
        up_move_change=1.25,
        down_move_change=0.9,
        num_periods=5)

    print 'Short Rate Lattice\n'
    short_rate.display(sig_digits=4)

    
    zcb = bl.BondLattice(
        interest_rate_lattice=short_rate,
        risk_free_probability=0.5,
        time_to_maturity=4,
        face_value=100)

    print 'ZCB t = 4 expiration: %s' % zcb.value()

    
    zcb_opt = bl.OptionPriceLattice(
        interest_rate_lattice=short_rate,
        risk_free_probability=0.5,
        option_style='american',
        option_type='put',
        strike_price=88,
        underlying_lattice=zcb,
        expiration=3)

    print 'ZCB American Put Option (t = 3, K = 88): %s' % zcb_opt.value()

    zcb_opt2 = bl.OptionPriceLattice(
        interest_rate_lattice=short_rate,
        risk_free_probability=0.5,
        option_style='european',
        option_type='call',
        strike_price=84,
        underlying_lattice=zcb,
        expiration=2)

    print 'ZCB European Call Option (t = 2, K = 84): %s' % zcb_opt2.value()


    b2 = bl.BondLattice(
        interest_rate_lattice=short_rate,
        risk_free_probability=0.5,
        time_to_maturity=6,
        coupon_rate=0.1,
        face_value=100)

    print '6 year 10%% Coupon Bond (t = 6): %s' % b2.value()
    #print '6 year 10%% Coupon Bond (t = 6)'
    #b2.display()

    #b2f = bl.BondForwardPriceLattice(
    #    interest_rate_lattice=short_rate,
    #    risk_free_probability=0.5,
    #    expiration=4,
    #    underlying_lattice=b2)
    print 'Bond Forward (t = 4): %s' % bl.calculate_bond_forward_price(b2, 4)

    b2f2 = bl.BondFuturesPriceLattice(
        risk_free_probability=0.5,
        expiration=4,
        underlying_lattice=b2)
    print 'Bond Futures (t = 4): %s' % b2f2.value()


    sw1 = bl.SwapLattice(
        interest_rate_lattice=short_rate,
        risk_free_probability=0.5,
        strike_rate=0.05,
        expiration=6)
    #sw1.display(sig_digits=4)
    print 'Swap w/ fixed rate 5%% and t = 6: %s' % sw1.value()

    sw1_opt = bl.OptionPriceLattice(
            interest_rate_lattice=short_rate,
            risk_free_probability=0.5,
            option_style='european',
            option_type='call',
            strike_price=0,
            underlying_lattice=sw1,
            expiration=3)
    #sw1_opt.display(sig_digits=4)
    print 'Swaption w/ strike = 0%% and t = 3: %s' % sw1_opt.value()
