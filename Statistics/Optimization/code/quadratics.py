"""
Gradient descent on two 2D strongly convex quadratics

    f(w) = 1/2 (w - w*)^T A (w - w*),   A = Q diag(mu, L) Q^T,

with step size eta = 1/L. Left panels: level sets of f and the GD path (red).
Right panels: empirical verification of the linear-convergence bounds
    f(w_k) - f*    <= (1 - mu/L)^k (f(w_0) - f*)                (objective)
    ||w_k - w*||^2 <= (2/mu) (1 - mu/L)^k (f(w_0) - f*)         (distance)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

K = 25


def make_quadratic(mu, L, theta):
    c, s = np.cos(theta), np.sin(theta)
    Q = np.array([[c, -s], [s, c]])
    return Q @ np.diag([mu, L]) @ Q.T


def run_gd(A, w_star, w0, eta, K):
    ws = [w0]
    for _ in range(K):
        ws.append(ws[-1] - eta * A @ (ws[-1] - w_star))
    return np.array(ws)


configs = [
    dict(mu=1.0, L=2.0, theta=np.pi / 6, w0=np.array([2.6, 1.0]), eta_mult=1.0, title=r"$\kappa = 2$"),
    dict(mu=1.0, L=10.0, theta=np.pi / 6, w0=np.array([2.6, 1.0]), eta_mult=1.8, title=r"$\kappa = 10$"),
]

w_star = np.zeros(2)
fig, axes = plt.subplots(2, 2, figsize=(10, 8.5), gridspec_kw=dict(width_ratios=[1, 1.1]))
ks = np.arange(K + 1)

for row, cfg in enumerate(configs):
    mu, L = cfg["mu"], cfg["L"]
    A = make_quadratic(mu, L, cfg["theta"])
    eta = cfg["eta_mult"] / L
    # eta <= 1/L: theorem rate 1 - eta*mu.  1/L < eta < 2/L: exact quadratic rate rho^2.
    rho = max(abs(1 - eta * mu), abs(1 - eta * L))
    rate = 1 - eta * mu if eta <= 1 / L + 1e-12 else rho**2
    rate_label = r"(1-\frac{1}{\kappa})^k" if eta <= 1 / L + 1e-12 else r"\rho^{2k}"
    ws = run_gd(A, w_star, cfg["w0"], eta, K)
    f = lambda W: 0.5 * np.einsum("...i,ij,...j->...", W, A, W)
    gap = f(ws)
    dist2 = np.sum(ws**2, axis=1)
    Delta = gap[0]
    kappa = L / mu

    # level sets + path
    ax = axes[row, 0]
    g = np.linspace(-3.2, 3.2, 400)
    X, Y = np.meshgrid(g, g)
    Z = f(np.stack([X, Y], axis=-1))
    levels = Delta * np.array([0.02, 0.06, 0.15, 0.3, 0.55, 1.0, 1.6])
    ax.contour(X, Y, Z, levels=levels, colors="#1f4e8c", linewidths=0.8)
    ax.plot(ws[:, 0], ws[:, 1], "-o", color="#b22222", ms=3.5, lw=1.5, label="GD iterates")
    ax.plot(*w_star, "k*", ms=10, label=r"$w^\ast$")
    ax.set_aspect("equal")
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2)
    ax.set_xlabel(r"$w_1$"); ax.set_ylabel(r"$w_2$")
    ax.set_title(f"Level sets and GD path, {cfg['title']} ($\\eta = {cfg['eta_mult']:g}/L$)")
    ax.legend(loc="lower left", fontsize=8)

    # bounds
    ax = axes[row, 1]
    ax.semilogy(ks, gap / Delta, "o-", color="#b22222", ms=3.5, zorder=3, label=r"$(f(w_k)-f^\ast)/\Delta$")
    ax.semilogy(ks, rate**ks, "--", color="#b22222", label=f"${rate_label}$ bound")
    ax.semilogy(ks, dist2 / (2 * Delta / mu), "s-", color="#1f4e8c", ms=3.5, alpha=0.8,
                label=r"$\|w_k-w^\ast\|^2 / (2\Delta/\mu)$")
    ax.set_ylim(1e-12, 3)
    ax.set_xlabel(r"iteration $k$")
    ax.set_title(f"Empirical check of bounds, {cfg['title']}")
    ax.grid(alpha=0.3, which="major")
    ax.legend(fontsize=8, loc="lower left")

    ok1 = np.all(gap <= Delta * rate**ks * (1 + 1e-9))
    ok2 = np.all(dist2 <= (2 * Delta / mu) * rate**ks * (1 + 1e-9))
    print(f"kappa={kappa:g}: objective bound holds={ok1}, distance bound holds={ok2}")

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "quadratics.png")
fig.savefig(out, dpi=150)
print("saved", os.path.normpath(out))
