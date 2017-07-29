#program to calculate how long it takes for bathtub to drain
import pint
import numpy as np
u = pint.UnitRegistry()
#=============Constants=======================#
g              = 9.8   * (u.meter/u.second**2)
#=============input Parameters================#
bathtub_vol    = 80    *  u.US_liquid_gallon
diameter_drain = 2     *  u.inch
bathtub_length = 60    *  u.inch
bathtub_width  = 30    *  u.inch
max_height     = 14.25 *  u.inch
faucet_flow    = 1     * (u.gallon/u.minute)
dt             = 0.01  *  u.second
#=============================================#
area_drain = np.pi * (diameter_drain/2)**2
water_height = (bathtub_vol/(bathtub_length*bathtub_width)).to(u.meter)

if water_height > max_height:
    print ' '
    print '    ERR: Too much water to fit in tub'
    print ' '
    exit()

flow_rate = (area_drain * np.sqrt(2 * g * water_height)).to(u.US_liquid_gallon/u.hour)

print ' '
print '=============Begin Program=============='
print 'flow rate:',flow_rate
print '========================================'

time = 0 * u.second
difference = 1 * u.inch

while difference.magnitude > 1e-10:
    old_height = water_height
    dh_faucet = (faucet_flow/(bathtub_length*bathtub_width))*dt
    if water_height.magnitude > 0:
        dh_tub = -(area_drain/(bathtub_length*bathtub_width)*np.sqrt(2*g*water_height))*dt
    else:
        dh_tub = 0 * u.meter
    water_height += dh_tub + dh_faucet
    difference = old_height - water_height
    time += dt

print 'time to empty:',time.to(u.minute)
#print '========================================'
