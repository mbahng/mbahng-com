[[1977sargent_dynamic-factor-models.pdf]]
#factors-and-components:factor-analysis:dynamic
[[1956bauer_simultaneous-iteration-method]], [[1977geweke_dynamic-fm]]

# Contribution 

   One of the first instances of dynamic factor models. 

# Background

## From Static to Dynamic Factor Models

**Static Factor Model (your baseline):**
$$y_t = \Lambda f_t + \varepsilon_t$$
where $y_t$ is $n \times 1$ observed variables, $f_t$ is $k \times 1$ factors, $\Lambda$ is $n \times k$ loadings, $\varepsilon_t$ is idiosyncratic error.

**Sargent-Sims Index Model** extends this to a dynamic setting with specific structure and distributed lag relationships.

## The General Index Model Framework

### Basic Structure
The authors propose models of the form:
$$(1) \quad y_t = a*z_t + u_t$$

Where:
- **$y_t$**: $n \times 1$ vector of observed dependent variables at time $t$
- **$z_t$**: $k \times 1$ vector of unobservable "indices" ($k \ll n$, typically $k=1,2,3$)
- **$a$**: $n \times k$ matrix of coefficients (factor loadings)
- **$u_t$**: $n \times 1$ vector of stochastic processes

### The Full Dynamic Structure with Distributed Lags

**Important clarification**: While equation (1) shows a static coefficient matrix $a$, the authors actually allow for a much richer dynamic relationship through **distributed lags**.

The complete dynamic relationship is represented by the convolution:
$$a*z(t) = \sum_{s=-\infty}^{\infty} a(s)z(t-s)$$

Where:
- **$a(s)$**: $n \times k$ coefficient matrices for the $s$-th lag of $z$
- **$a(0)$**: corresponds to the matrix $a$ in equation (1) (contemporaneous effects)
- **$a(1), a(2), ...$**: represent lagged effects of indices on observed variables

**One-sided restriction**: $a(s) = 0$ for $s < 0$, meaning only current and past values of indices affect current observations.

So the full model is actually:
$$y_t = a(0)z_t + a(1)z_{t-1} + a(2)z_{t-2} + ... + u_t$$

Each $a(s)$ is an $n \times k$ matrix, and each term $a(s)z_{t-s}$ involves standard matrix multiplication producing an $n \times 1$ vector.

### The Need for Matrix Inversion: Solving the System

The indices themselves follow dynamic processes. For example:
$$z_t = c_1 z_{t-1} + c_2 z_{t-2} + ... + \varepsilon_t$$

Substituting this into the distributed lag equation creates a system where current $y_t$ depends on its own past values. Using lag operator notation $L$ (where $Ly_t = y_{t-1}$):

$$y_t = a(L)z_t + u_t$$
$$z_t = c(L)z_{t-1} + \varepsilon_t$$

This leads to:
$$(I - a(L)c(L))y_t = a(L)\varepsilon_t + u_t$$

**Why the inverse $(I - a*c_i)^{-1}$ is needed:**

1. **To solve for the reduced form**: We need to express $y_t$ in terms of current and past shocks only:
   $$y_t = (I - a(L)c(L))^{-1}[a(L)\varepsilon_t + u_t]$$

2. **To ensure system stability**: The inverse exists only when the eigenvalues of the lag polynomial are inside the unit circle, ensuring shocks eventually die out.

3. **To enable forecasting**: Without the inverse, we cannot generate multi-step ahead forecasts or compute impulse response functions.

4. **For identification**: The inverse allows us to recover structural parameters from the reduced form.

### Key Dynamic Restrictions

1. **Static structural relationship**: The lag coefficients $a(s)$ are time-invariant
2. **Serial correlation structure**: **$z_t$ and $u_t$ are uncorrelated at all leads and lags**
3. **Invertibility condition**: **$(I - a*c_i)$ has a one-sided inverse under convolution**

The third condition ensures the system can be solved forward and is technically required for identification.

## Two Types of Index Models

### Type 1: Observable-Index Models

**Definition**: $z_t$ can be written as a function of observable $y$'s.

**Mathematical Form**:
$$z_t = \text{orthogonal projection of } y_t \text{ onto space spanned by } \{y_s: s \leq t\}$$

**Example Structure**:
If $z_t$ is scalar and depends on current and past $y$:
$$z_t = \sum_{j=0}^{\infty} \gamma_j y_{t-j}$$

**Economic Interpretation**: The index represents a "sufficient statistic" that captures all relevant information from the observable variables' history.

### Type 2: Unobservable-Index Models  

**Definition**: $z_t$ cannot be expressed as a function of observable variables alone.

**Specification**: Both $z_t$ and $u_t$ follow independent stochastic processes, typically:
$$z_t = \text{autoregressive process (e.g., AR(p))}$$
$$u_t = \text{vector autoregressive process (e.g., VAR(q))}$$

## Detailed Mathematical Specification

### The Complete System with Explicit Inversion

Starting from the structural form and incorporating index dynamics, the system becomes:
$$(2) \quad (I - a*c_i)y_t = a*c_0*x_0 + u_t$$

Where:
- **$c_i$**: coefficient matrices in the lag polynomial representation of $z_t$
- **$I$**: identity matrix
- **$x_0$**: initial conditions for the $z$ process

**The reduced form** requires inversion:
$$y_t = (I - a*c_i)^{-1}[a*c_0*x_0 + u_t]$$

This inversion is **mathematically necessary** because:
- We need to solve the simultaneous system
- Current $y_t$ depends on current $z_t$, but $z_t$ has its own dynamics
- Without inversion, we cannot separate structural shocks from reduced-form residuals

### Spectral Density Representation

For frequency domain analysis, they show the spectral density matrix of $y_t$ is:

$$(3) \quad S_y(\omega) = a(\omega)S_z(\omega)a(\omega)' + S_u(\omega)$$

Where:
- **$S_y(\omega)$**: spectral density matrix of observed variables at frequency $\omega$
- **$S_z(\omega)$**: spectral density matrix of indices ($k \times k$)
- **$S_u(\omega)$**: spectral density matrix of idiosyncratic components ($n \times n$)
- **$a(\omega)$**: Fourier transform of the distributed lag coefficients $a(s)$

### Estimation via Maximum Likelihood

**For Unobservable-Index Models:**

The likelihood function (assuming Gaussian processes):
$$L(C,\tilde{z},\ldots,\tilde{z}_m) = -\frac{m}{\pi|C|} \exp\left(-\sum \tilde{z}_i(\omega)C^{-1}\tilde{z}_i(\omega)\right)$$

Where:
- **$C$**: covariance matrix estimate
- **$\tilde{z}_i(\omega)$**: Fourier transform of $y_i$ evaluated at frequency $\omega$
- **$m$**: number of observations

**Estimation Steps:**
1. Estimate spectral density matrix $S_y$ at multiple frequencies
2. Decompose $S_y = LL' + V$ (where $L$ corresponds to '$a(\omega)$', $V$ to $S_u$)
3. Use frequency domain maximum likelihood
4. Apply inverse Fourier transform to get time domain parameters

## Economic Interpretation Framework

### The "Index" Concept

**Economic Meaning**: Each index $z_t$ represents an unobservable economic force:
- $z_1$ might represent "aggregate demand pressure"
- $z_2$ might represent "monetary/nominal shocks"  
- $z_3$ might represent "supply-side disturbances"

### Loading Matrix and Distributed Lag Interpretation

The distributed lag structure shows how each unobservable index affects each observable variable over time:

$$\begin{bmatrix}
\text{GNP}_t \\
\text{UNEMP}_t \\
\text{PRICE}_t \\
\text{WAGE}_t
\end{bmatrix} = 
\begin{bmatrix}
a_{11}(0) & a_{12}(0) \\
a_{21}(0) & a_{22}(0) \\
a_{31}(0) & a_{32}(0) \\
a_{41}(0) & a_{42}(0)
\end{bmatrix}
\begin{bmatrix}
z_{1t} \\
z_{2t}
\end{bmatrix} + 
\begin{bmatrix}
a_{11}(1) & a_{12}(1) \\
a_{21}(1) & a_{22}(1) \\
a_{31}(1) & a_{32}(1) \\
a_{41}(1) & a_{42}(1)
\end{bmatrix}
\begin{bmatrix}
z_{1,t-1} \\
z_{2,t-1}
\end{bmatrix} + \ldots$$

- **$a_{11}(0)$**: contemporaneous effect of first index on GNP
- **$a_{11}(1)$**: one-period lagged effect of first index on GNP
- **$a_{21}(0)$**: contemporaneous effect of first index on unemployment

### Dynamic Propagation and the Role of Inversion

The indices $z_t$ themselves have dynamic structure:
$$z_{1t} = \rho_1 z_{1,t-1} + \varepsilon_{1t}$$
$$z_{2t} = \rho_2 z_{2,t-1} + \varepsilon_{2t}$$

Combined with the distributed lag effects, this creates **complex propagation patterns**. A shock $\varepsilon_{1t}$ affects:

1. **All variables directly** through $a_{\cdot 1}(0), a_{\cdot 1}(1)$, etc. at times $t, t+1, \ldots$
2. **All variables through index persistence** as $z_{1,t+1} = \rho_1 z_{1t} + \varepsilon_{1,t+1}$
3. **The entire system's future path** through the inverted system dynamics

**The matrix inversion $(I - a*c_i)^{-1}$ captures all these feedback effects**, allowing us to trace how a single structural shock propagates through the entire economy over time.

## Why the Inverse is Economically Essential

### 1. **Structural vs. Reduced Form**
- **Structural**: $y_t = a(L)z_t + u_t$ with $z_t = c(L)z_{t-1} + \varepsilon_t$
- **Reduced Form**: $y_t = (I - a(L)c(L))^{-1}[a(L)\varepsilon_t + u_t]$

### 2. **Economic Interpretation**
The inverse transforms **unobservable structural shocks** $\varepsilon_t$ into **observable outcomes** $y_t$, accounting for all the dynamic feedback in the economy.

### 3. **Policy Analysis**
Without the inverse, we cannot answer questions like:
- What happens to unemployment if monetary policy shocks the economy?
- How long do demand shocks take to affect prices?
- What are the dynamic multipliers of fiscal policy?

## Key Differences from Static Factor Models

1. **Temporal Structure**: 
   - Explicit modeling of how factors evolve over time
   - Distributed lag effects from factors to observables
   - System-wide feedback through matrix inversion

2. **Identification**: 
   - Uses cross-equation restrictions and temporal correlation patterns
   - Frequency domain methods exploit different correlation patterns across frequencies
   - Invertibility conditions ensure unique structural identification

3. **Frequency Domain Focus**: 
   - Heavy use of spectral analysis for estimation
   - Different economic forces may dominate at different frequencies (business cycle vs. short-run)

4. **Economic Interpretation**: 
   - Factors represent economic "shocks" or "innovations" 
   - Distributed lags capture realistic adjustment dynamics
   - Matrix inversion reveals system-wide propagation mechanisms

5. **Forecasting Framework**: 
   - Natural multi-step-ahead prediction through factor evolution
   - Accounts for both direct and indirect (through lags and feedbacks) transmission of shocks

## The Innovation of the Approach

This framework was groundbreaking because it:
- Provided a middle ground between atheoretical VARs and heavily restricted structural models
- Let the data determine both the number of common factors and their dynamic properties
- Recognized that economic relationships involve complex lag structures and feedback effects
- Used frequency domain methods to identify different types of economic fluctuations
- Made the connection between unobservable economic forces and observable outcomes mathematically rigorous

The distributed lag structure combined with the matrix inversion makes this much richer than simple static factor models, allowing for realistic economic adjustment processes while maintaining the parsimony of a low-dimensional factor structure. The mathematical requirement for inversion is not just technical—it's fundamental to understanding how economies respond to shocks over time.

