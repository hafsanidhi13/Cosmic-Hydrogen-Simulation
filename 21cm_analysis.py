import numpy as np
import matplotlib.pyplot as plt

# Define redshift range (fewer points for faster computation)
z = np.linspace(30, 5, 30)  # 30 redshifts from 30 to 5

# Standard model parameters
std_params = {
    'hubble': 0.69,
    'matter': 0.31,
    'baryon': 0.02
}

# Parameter variations
hubble_variations = [0.67, 0.69, 0.71]  # Low, Standard, High
matter_variations = [0.29, 0.31, 0.33]  # Low, Standard, High
baryon_variations = [0.018, 0.02, 0.022]  # Low, Standard, High

def calculate_mean_temperature(redshift, hubble, matter, baryon):
    """Calculate mean brightness temperature for given parameters"""
    bt = T_b(box=50, redshift=redshift, hubble=hubble, 
             matter=matter, baryon=baryon)
    return np.mean(bt.brightness_temp)

print("Computing brightness temperatures...")
print("="*50)

# 1. Standard model
print("1. Computing standard model...")
Tb_std = []
for i, redshift in enumerate(z):
    Tb_std.append(calculate_mean_temperature(redshift, 
                                             std_params['hubble'],
                                             std_params['matter'],
                                             std_params['baryon']))
    print(f"   z={redshift:.1f}: {Tb_std[-1]:.2f} mK ({i+1}/{len(z)})")
Tb_std = np.array(Tb_std)

# 2. Hubble parameter variations
print("\n2. Computing Hubble parameter variations...")
Tb_hubble = {}
for h in hubble_variations:
    print(f"  Hubble = {h}")
    Tb_hubble[h] = []
    for i, redshift in enumerate(z):
        Tb_hubble[h].append(calculate_mean_temperature(redshift, h, 
                                                       std_params['matter'],
                                                       std_params['baryon']))
        if i % 10 == 0:  # Print progress every 10 redshifts
            print(f"    z={redshift:.1f}: {Tb_hubble[h][-1]:.2f} mK")
    Tb_hubble[h] = np.array(Tb_hubble[h])

# 3. Matter density variations
print("\n3. Computing matter density variations...")
Tb_matter = {}
for m in matter_variations:
    print(f"  Matter = {m}")
    Tb_matter[m] = []
    for i, redshift in enumerate(z):
        Tb_matter[m].append(calculate_mean_temperature(redshift, 
                                                       std_params['hubble'],
                                                       m,
                                                       std_params['baryon']))
        if i % 10 == 0:
            print(f"    z={redshift:.1f}: {Tb_matter[m][-1]:.2f} mK")
    Tb_matter[m] = np.array(Tb_matter[m])

# 4. Baryon density variations
print("\n4. Computing baryon density variations...")
Tb_baryon = {}
for b in baryon_variations:
    print(f"  Baryon = {b}")
    Tb_baryon[b] = []
    for i, redshift in enumerate(z):
        Tb_baryon[b].append(calculate_mean_temperature(redshift, 
                                                       std_params['hubble'],
                                                       std_params['matter'],
                                                       b))
        if i % 10 == 0:
            print(f"    z={redshift:.1f}: {Tb_baryon[b][-1]:.2f} mK")
    Tb_baryon[b] = np.array(Tb_baryon[b])

print("\n" + "="*50)
print("Creating plots...")

# Create figure with subplots
fig = plt.figure(figsize=(18, 12))

# Colors for different parameters
colors_h = ['blue', 'black', 'red']  # Hubble
colors_m = ['green', 'black', 'purple']  # Matter
colors_b = ['orange', 'black', 'brown']  # Baryon

# 1. All variations together
ax1 = plt.subplot(2, 3, 1)
ax1.plot(z, Tb_std, 'k-', linewidth=3, label='Standard Model', alpha=0.8)

# Hubble variations
for h, color in zip(hubble_variations, colors_h):
    if h == std_params['hubble']:
        continue  # Skip standard (already plotted)
    label = f'h = {h}'
    ax1.plot(z, Tb_hubble[h], color=color, linestyle='--', 
             linewidth=2, label=label, alpha=0.7)

# Matter variations
for m, color in zip(matter_variations, colors_m):
    if m == std_params['matter']:
        continue
    label = f'Ωₘ = {m}'
    ax1.plot(z, Tb_matter[m], color=color, linestyle=':', 
             linewidth=2, label=label, alpha=0.7)

# Baryon variations
for b, color in zip(baryon_variations, colors_b):
    if b == std_params['baryon']:
        continue
    label = f'Ω_b = {b}'
    ax1.plot(z, Tb_baryon[b], color=color, linestyle='-.', 
             linewidth=2, label=label, alpha=0.7)

ax1.set_xlabel('Redshift (z)', fontsize=12)
ax1.set_ylabel('Mean Brightness Temperature [mK]', fontsize=12)
ax1.set_title('All Parameter Variations', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='best', fontsize=9)
ax1.invert_xaxis()  # Show high to low redshift

# 2. Hubble parameter variations
ax2 = plt.subplot(2, 3, 2)
ax2.plot(z, Tb_std, 'k-', linewidth=3, label='Standard Model')

for h, color in zip(hubble_variations, colors_h):
    if h == std_params['hubble']:
        continue
    diff = (Tb_hubble[h] - Tb_std) / Tb_std * 100
    ax2.plot(z, Tb_hubble[h], color=color, linewidth=2, 
             label=f'h = {h}')

ax2.set_xlabel('Redshift (z)', fontsize=12)
ax2.set_ylabel('Mean Brightness Temperature [mK]', fontsize=12)
ax2.set_title('Hubble Parameter (h) Variations', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='best')
ax2.invert_xaxis()

# 3. Matter density variations
ax3 = plt.subplot(2, 3, 3)
ax3.plot(z, Tb_std, 'k-', linewidth=3, label='Standard Model')

for m, color in zip(matter_variations, colors_m):
    if m == std_params['matter']:
        continue
    ax3.plot(z, Tb_matter[m], color=color, linewidth=2,
             label=f'Ωₘ = {m}')

ax3.set_xlabel('Redshift (z)', fontsize=12)
ax3.set_ylabel('Mean Brightness Temperature [mK]', fontsize=12)
ax3.set_title('Matter Density (Ωₘ) Variations', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(loc='best')
ax3.invert_xaxis()

# 4. Baryon density variations
ax4 = plt.subplot(2, 3, 4)
ax4.plot(z, Tb_std, 'k-', linewidth=3, label='Standard Model')

for b, color in zip(baryon_variations, colors_b):
    if b == std_params['baryon']:
        continue
    ax4.plot(z, Tb_baryon[b], color=color, linewidth=2,
             label=f'Ω_b = {b}')

ax4.set_xlabel('Redshift (z)', fontsize=12)
ax4.set_ylabel('Mean Brightness Temperature [mK]', fontsize=12)
ax4.set_title('Baryon Density (Ω_b) Variations', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(loc='best')
ax4.invert_xaxis()

# 5. Percentage differences
ax5 = plt.subplot(2, 3, 5)

for h, color in zip(hubble_variations, colors_h):
    if h == std_params['hubble']:
        continue
    diff = (Tb_hubble[h] - Tb_std) / Tb_std * 100
    ax5.plot(z, diff, color=color, linestyle='--', linewidth=2,
             label=f'h = {h}')

for m, color in zip(matter_variations, colors_m):
    if m == std_params['matter']:
        continue
    diff = (Tb_matter[m] - Tb_std) / Tb_std * 100
    ax5.plot(z, diff, color=color, linestyle=':', linewidth=2,
             label=f'Ωₘ = {m}')

for b, color in zip(baryon_variations, colors_b):
    if b == std_params['baryon']:
        continue
    diff = (Tb_baryon[b] - Tb_std) / Tb_std * 100
    ax5.plot(z, diff, color=color, linestyle='-.', linewidth=2,
             label=f'Ω_b = {b}')

ax5.set_xlabel('Redshift (z)', fontsize=12)
ax5.set_ylabel('Percentage Difference from Standard [%]', fontsize=12)
ax5.set_title('Relative Differences', fontsize=14, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax5.legend(loc='best', fontsize=9)
ax5.invert_xaxis()

# 6. Final redshift comparison (z=5)
ax6 = plt.subplot(2, 3, 6)

parameters = ['Standard']
values = [Tb_std[-1]]
colors = ['black']

# Add Hubble variations
for h, color in zip(hubble_variations, colors_h):
    if h == std_params['hubble']:
        continue
    parameters.append(f'h={h}')
    values.append(Tb_hubble[h][-1])
    colors.append(color)

# Add Matter variations
for m, color in zip(matter_variations, colors_m):
    if m == std_params['matter']:
        continue
    parameters.append(f'Ωₘ={m}')
    values.append(Tb_matter[m][-1])
    colors.append(color)

# Add Baryon variations
for b, color in zip(baryon_variations, colors_b):
    if b == std_params['baryon']:
        continue
    parameters.append(f'Ω_b={b}')
    values.append(Tb_baryon[b][-1])
    colors.append(color)

# Create bar chart
x_pos = np.arange(len(parameters))
bars = ax6.bar(x_pos, values, color=colors, alpha=0.7)
ax6.set_xlabel('Parameter Set', fontsize=12)
ax6.set_ylabel('Brightness Temp at z=5 [mK]', fontsize=12)
ax6.set_title('Comparison at z=5', fontsize=14, fontweight='bold')
ax6.set_xticks(x_pos)
ax6.set_xticklabels(parameters, rotation=45, ha='right')
ax6.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.1f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.suptitle('21cm Brightness Temperature: Parameter Sensitivity', 
             fontsize=16, fontweight='bold', y=1.02)
plt.show()

# Save figure
fig.savefig('parameter_sensitivity.png', dpi=150, bbox_inches='tight')
print("Figure saved as 'parameter_sensitivity.png'")

# Print summary
print("\n" + "="*60)
print("SUMMARY AT z=5")
print("="*60)
print(f"Standard Model: {Tb_std[-1]:.2f} mK")

print("\nHubble variations:")
for h in hubble_variations:
    if h != std_params['hubble']:
        diff = (Tb_hubble[h][-1] - Tb_std[-1]) / Tb_std[-1] * 100
        print(f"  h={h}: {Tb_hubble[h][-1]:.2f} mK (Δ={diff:+.1f}%)")

print("\nMatter density variations:")
for m in matter_variations:
    if m != std_params['matter']:
        diff = (Tb_matter[m][-1] - Tb_std[-1]) / Tb_std[-1] * 100
        print(f"  Ωₘ={m}: {Tb_matter[m][-1]:.2f} mK (Δ={diff:+.1f}%)")

print("\nBaryon density variations:")
for b in baryon_variations:
    if b != std_params['baryon']:
        diff = (Tb_baryon[b][-1] - Tb_std[-1]) / Tb_std[-1] * 100
        print(f"  Ω_b={b}: {Tb_baryon[b][-1]:.2f} mK (Δ={diff:+.1f}%)")