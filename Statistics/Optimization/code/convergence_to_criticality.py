"""
Gradient descent with eta = 1/L on a nonconvex L-smooth function, tracking the gradient norm
until it reaches epsilon = 0.1, and comparing against the guarantee

    min_{k < K} ||grad f(w_k)|| <= sqrt(2 L (f(w_0) - inf f) / K).

Test function:
    f(x, y) = 0.15 x^2 + 5 y^2 + 2 sin(x) sin(y)

Hessian = diag(0.3, 10) + 2 * [[-sin x sin y, cos x cos y], [cos x cos y, -sin x sin y]];
the second matrix has eigenvalues cos(x+y), -cos(x-y) in [-1, 1], so ||Hessian|| <= 10 + 2 = 12 =: L.
The very flat x-direction (curvature 0.3) makes GD slow, and the sin terms make f nonconvex.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

L = 12.0
EPS = 0.1


def f(w):
    x, y = w
    return 0.15 * x**2 + 5 * y**2 + 2 * np.sin(x) * np.sin(y)


def grad(w):
    x, y = w
    return np.array([0.3 * x + 2 * np.cos(x) * np.sin(y),
                     10 * y + 2 * np.sin(x) * np.cos(y)])


def global_min_value():
    # f >= 0.15 x^2 + 5 y^2 - 2, so the global minimum lies in a small box; grid search + GD polish
    xs = np.linspace(-6, 6, 1201)
    ys = np.linspace(-2, 2, 401)
    X, Y = np.meshgrid(xs, ys)
    Z = f([X, Y])
    i = np.unravel_index(np.argmin(Z), Z.shape)
    w = np.array([X[i], Y[i]])
    for _ in range(100000):
        w = w - grad(w) / L
    return f(w), w


def wiggly_valley():
    K = 100
    eta = 1.0 / L
    w0 = np.array([8.0, 1.0])

    ws = [w0]
    for _ in range(K):
        ws.append(ws[-1] - eta * grad(ws[-1]))
    ws = np.array(ws)
    fs = np.array([f(w) for w in ws])
    gn = np.array([np.linalg.norm(grad(w)) for w in ws])
    running_min = np.minimum.accumulate(gn)

    f_inf, w_star = global_min_value()
    ks = np.arange(1, K + 1)
    # min over k in [K-1] = {0, ..., K-1}: running_min[K-1]
    thm_bound = np.sqrt(2 * L * (fs[0] - f_inf) / ks)
    assert np.all(running_min[ks - 1] <= thm_bound + 1e-12), "Theorem violated!"

    first = int(np.argmax(gn <= EPS))
    assert gn[first] <= EPS
    K_guarantee = 2 * L * (fs[0] - f_inf) / EPS**2
    print(f"L = {L}, eta = {eta:.4f}, eps = {EPS}, w_0 = {w0}")
    print(f"f(w_0) = {fs[0]:.4f}, inf f = {f_inf:.6f} at {np.round(w_star, 3)}")
    print(f"First k with ||grad f(w_k)|| <= eps: {first}   (||grad|| = {gn[first]:.4f})")
    print(f"Theorem's guaranteed K for eps: {K_guarantee:.0f}")
    print(f"Theorem bound at K = {K}: {thm_bound[-1]:.3f}; actual min ||grad||: {running_min[K - 1]:.4f}")

    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
    ax = axes[0]
    xs = np.linspace(-3, 9, 400)
    ys = np.linspace(-2, 2.2, 300)
    X, Y = np.meshgrid(xs, ys)
    hm = ax.pcolormesh(X, Y, f([X, Y]), cmap="viridis", shading="auto")
    fig.colorbar(hm, ax=ax, label="$f(x,y)$")
    ax.plot(ws[:, 0], ws[:, 1], "-o", color="red", markersize=2.5, linewidth=1.0)
    ax.plot(*ws[0], "o", color="red", markersize=7, markeredgecolor="white")
    ax.set_xlim(xs[0], xs[-1])
    ax.set_ylim(ys[0], ys[-1])
    ax.set_title("Gradient descent trajectory")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

    ax = axes[1]
    ax.semilogy(gn, color="tab:blue", label=r"$\|\nabla f(w_k)\|$")
    ax.axhline(EPS, color="gray", linestyle="--", label=r"$\epsilon = 0.1$")
    ax.plot(first, gn[first], "o", color="red", label=f"first $k$ with $\\|\\nabla f\\| \\leq \\epsilon$: {first}")
    ax.set_title("Gradient norm")
    ax.set_xlabel("iteration $k$")
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[2]
    ax.loglog(ks, thm_bound, "--", color="tab:orange",
              label=r"$\sqrt{2L(f(w_0)-\inf f)/K}$")
    ax.loglog(ks, running_min[ks - 1], color="tab:blue", label=r"$\min_{k<K}\|\nabla f(w_k)\|$")
    ax.axhline(EPS, color="gray", linestyle="--")
    ax.set_title("Theorem bound vs. actual")
    ax.set_xlabel("$K$")
    ax.legend()
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "convergence_to_criticality.png")
    fig.savefig(out, dpi=150)
    print("Saved", os.path.normpath(out))


# ---------------------------------------------------------------------------------------------
# Near-extremal example: a long, nearly constant-slope ramp.
#   f(x, y) = s*delta*(sqrt(1 + (x/delta)^2) - 1) + 6 y^2,   delta = s / L
# The x-part is a pseudo-Huber function: slope -> s as |x| -> infinity, curvature <= s/delta = L.
# With s slightly above eps, GD (eta = 1/L) moves only s/L per step and decreases f by ~ s^2/L per
# step, so it needs ~ L*Delta/s^2 steps, versus the guarantee 2 L Delta / eps^2: within a factor ~2.
# ---------------------------------------------------------------------------------------------
S_RAMP = 0.101
DELTA = S_RAMP / L


def f_ramp(w):
    x, y = w
    return S_RAMP * DELTA * (np.sqrt(1 + (x / DELTA) ** 2) - 1) + 6 * y**2


def grad_ramp(w):
    x, y = w
    return np.array([S_RAMP * x / np.sqrt(DELTA**2 + x**2), 12 * y])


def ramp():
    eta = 1.0 / L
    w = np.array([1000.0, 1.0])
    f0 = f_ramp(w)
    f_inf = 0.0  # attained at the origin
    gn, fs, xs_traj = [], [], []
    first = None
    k = 0
    while True:
        g = grad_ramp(w)
        n = np.linalg.norm(g)
        gn.append(n)
        fs.append(f_ramp(w))
        xs_traj.append(w[0])
        if n <= EPS:
            first = k
            break
        w = w - eta * g
        k += 1
    gn = np.array(gn)
    fs = np.array(fs)
    running_min = np.minimum.accumulate(gn)
    Ks = np.unique(np.logspace(0, np.log10(first), 400).astype(int))
    Ks = Ks[Ks >= 1]
    thm_bound = np.sqrt(2 * L * (f0 - f_inf) / Ks)
    assert np.all(running_min[Ks - 1] <= thm_bound + 1e-12), "Theorem violated!"
    K_guarantee = 2 * L * (f0 - f_inf) / EPS**2
    print(f"\n[ramp] s = {S_RAMP}, w_0 = (1000, 1), f(w_0) = {f0:.3f}")
    print(f"[ramp] first k with ||grad f(w_k)|| <= eps: {first}")
    print(f"[ramp] guaranteed K: {K_guarantee:.0f}  ->  ratio first/guarantee = {first / K_guarantee:.3f}")

    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
    ax = axes[0]
    xx = np.linspace(-2, 20, 600)
    ax.plot(xx, [f_ramp([x, 0]) for x in xx], color="tab:blue")
    ax.set_title(r"Profile $f(x, 0)$: a long ramp of slope $s \approx 0.101$")
    ax.set_xlabel("$x$")
    ax.grid(alpha=0.3)

    ax = axes[1]
    ax.semilogy(gn, color="tab:blue", label=r"$\|\nabla f(w_k)\|$")
    ax.axhline(EPS, color="gray", linestyle="--", label=r"$\epsilon = 0.1$")
    ax.plot(first, gn[first], "o", color="red", label=f"first $k$ with $\\|\\nabla f\\| \\leq \\epsilon$: {first}")
    ax.set_title("Gradient norm")
    ax.set_xlabel("iteration $k$")
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[2]
    ax.loglog(Ks, thm_bound, "--", color="tab:orange", label=r"$\sqrt{2L(f(w_0)-\inf f)/K}$")
    ax.loglog(Ks, running_min[Ks - 1], color="tab:blue", label=r"$\min_{k<K}\|\nabla f(w_k)\|$")
    ax.axhline(EPS, color="gray", linestyle="--")
    ax.axvline(K_guarantee, color="tab:orange", linestyle=":", label=f"guaranteed $K \\approx {K_guarantee:.2g}$")
    ax.set_title("Theorem bound vs. actual")
    ax.set_xlabel("$K$")
    ax.legend()
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "convergence_to_criticality_ramp.png")
    fig.savefig(out, dpi=150)
    print("[ramp] Saved", os.path.normpath(out))


if __name__ == "__main__":
    wiggly_valley()
    ramp()
