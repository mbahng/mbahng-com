
function simplify(frac) {
    if (frac[1] == 0 && frac[0] < 0) { return [-frac[0], frac[1]];}
    if (frac[0] == 0 || frac[1] == 0) {return frac;}
    var gcd = function gcd(a, b) {
        return b ? gcd(b, a%b) : a; 
    };
    gcd = gcd(frac[0], frac[1]); 
    var simplified_output = [frac[0]/gcd, frac[1]/gcd]; 
    if (simplified_output[0] < 0) {
        simplified_output = [-frac[0]/gcd, -frac[1]/gcd]; 
    } 
    return simplified_output
}

const allEqual = arr => arr.every(val => val === arr[0]);

function clean(frac, addsign=true) {
    if (frac[0] % frac[1] == 0) {
        var integer = frac[0] / frac[1]; 
        if (integer == 1 && addsign==false) {
            return ``;
        } else if (integer == -1 && addsign==false) {
            return `-`;
        } else if (integer > 0) {
            return (addsign ? ` + ${integer}` : ` ${integer}`);
        } else if (integer < 0) {
            return ` ${integer}`; 
        } else {
            return ` `;
        }
    } else if ((frac[0]/frac[1]) > 0) {
        frac = simplify(frac);
        return (addsign ? ` + \\frac{${frac[0]}}{${frac[1]}}` : ` \\frac{${frac[0]}}{${frac[1]}}`);
    } else if ((frac[0]/frac[1]) == 0) {
        return ` `;
    } else if ((frac[0]/frac[1]) < 0) { 
        frac = simplify(frac);
        var neg_count = 0; 
        var plus_minus = '';
        if (frac[0] < 0) {neg_count += 1; frac[0] = - frac[0];}
        if (frac[1] < 0) {neg_count += 1; frac[1] = - frac[1];}
        if (neg_count % 2 == 1) {plus_minus = '-'}
        return ` ${plus_minus} \\frac{${frac[0]}}{${frac[1]}}`;
    }
}

function randNumGen(level) {
    /* Level 1: Returns a random integer between 0 and 5
       Level 2; Returns random number with step size .5 between -5 and 5
    */
    
    if (level == 1) {
        var integer = Math.round((Math.random() * 10) - 5);
        return [integer, 1]; 

    } else if (level == 2) {
        numerator = Math.round((Math.random() * 20) - 10); 
        denominator = Math.round((Math.random() * 3) + 1); 
        return [numerator, denominator];

    } else if (level == 3) {
        numerator = Math.round((Math.random() * 20)); 
        denominator = Math.round((Math.random() * 7) + 1); 
        return [numerator, denominator];
    }
}

function fracSum(frac1, frac2) {
    const numerator = frac1[0] * frac2[1] + frac1[1] * frac2[0]; 
    const denominator = frac1[1] * frac2[1];
    return simplify([numerator, denominator]);
}

function fracProd(frac1, frac2) {
    return simplify([frac1[0] * frac2[0], frac1[1] * frac2[1]]);
}

function LinSI_PS(level) {
    // Generating a linear equation to convert from slope-intercept to point-slope
    var slope = randNumGen(level);
    while (clean(slope) == ` `) {
        slope = randNumGen(level); }
    var y_int = randNumGen(level);
    var y_point_at_x1 = fracSum(y_int, slope); 
    return [`Convert to Point-Slope Form: $y = ${clean(slope, addsign=false)}x ${clean(y_int, addsign=true)}$`,`$y ${clean([-y_point_at_x1[0], y_point_at_x1[1]])} = ${clean(slope, addsign=false)} (x - 1)$`]; 
}

function LinPS_SI(level) {
    // Generating a linear equation to convert from point-slope to slope-intercept
    var slope = randNumGen(level);
    while (clean(slope) == ` `) {
        slope = randNumGen(level); }
    var x_pnt = randNumGen(level);
    var y_pnt = randNumGen(level);
    var neg_x_pnt = [-x_pnt[0], x_pnt[1]];
    var neg_y_pnt = [-y_pnt[0], y_pnt[1]];

    var y_int = fracSum(fracProd(slope, neg_x_pnt), y_pnt);
    return [`Convert to Slope-Intercept Form: $y ${clean(neg_y_pnt, addsign=true)} = ${clean(slope, addsign=false)} (x ${clean(neg_x_pnt, addsign=true)})$`, `$y = ${clean(slope, addsign=false)} x ${clean(y_int)}$`]

}

function QuadS_F(level) {
    // Generating a quadratic equation to convert from standard to vertex
    if (level == 1) {
        var c = [Math.round((Math.random() * 30) - 15), 1]; 
        var d = [Math.round((Math.random() * 24) - 12), 1]; 
        var lin_coef = fracSum(c, d); 
        var const_coef = fracProd(c, d); 


        var lin_term; 
        if (lin_coef[0] == 0) {
            lin_term = ``;
        } else {lin_term = `${clean(lin_coef, addsign=true)}x`;}
        var const_term = `${clean(const_coef, addsign=true)}`

        if (c[0] == d[0]) {
            return [`Factor: $x^2 ${lin_term} ${const_term}$`, `$(x ${clean(c, addsign=true)})^2$`];
        } else {
            return [`Factor: $x^2 ${lin_term} ${const_term}$`, `$(x ${clean(c, addsign=true)})(x ${clean(d, addsign=true)})$`];
        }
        
        
    } else if (level == 2) {
        var multiplier = [Math.round((Math.random() * 4) -2), 1];
        while (multiplier[0] == 0) {
            multiplier = [Math.round((Math.random() * 4) -2), 1];
        }
        var a = [Math.round((Math.random() * 2) + 1), 1];
        var b = [Math.round((Math.random() * 2) + 1), 1];
        var c = [Math.round((Math.random() * 30) - 15), 1]; 
        var d = [Math.round((Math.random() * 24) - 12), 1]; 

        const simple1 = simplify([a[0], c[0]]);
        const simple2 = simplify([b[0], d[0]]);
        a = [simple1[0], 1];
        c = [simple1[1], 1];
        b = [simple2[0], 1];
        d = [simple2[1], 1];

        quad_coef = fracProd(multiplier, fracProd(a, b)); 
        lin_coef = fracProd(multiplier, fracSum(fracProd(a, d), fracProd(b, c))); 
        const_coef = fracProd(multiplier, fracProd(c, d)); 

        var quad_term = `${clean(quad_coef, addsign=false)}x^2` 
        var lin_term; 
        if (lin_coef[0] == 0) {
            lin_term = ``;
        } else {lin_term = `${clean(lin_coef, addsign=true)}x`;}
        var const_term = `${clean(const_coef, addsign=true)}`

        if (a[0] == b[0] && c[0] == d[0]) {
            return [`Factor: $ ${quad_term} ${lin_term} ${const_term}$`, `$${clean(multiplier, addsign=false)} (${clean(a, addsign=false)} x ${clean(c, addsign=true)})^2$`]
        } else {
            return [`Factor: $ ${quad_term} ${lin_term} ${const_term}$`, `$${clean(multiplier, addsign=false)} (${clean(a, addsign=false)} x ${clean(c, addsign=true)})(${clean(b, addsign=false)} x ${clean(d, addsign=true)})$`]
        }


    } else if (level == 3) {
        var multiplier = [Math.round((Math.random() * 8) -4), 1];
        while (multiplier[0] == 0) {
            multiplier = [Math.round((Math.random() * 8) -4), 1];
        }
        var a = [Math.round((Math.random() * 4) + 1), 1];
        var b = [Math.round((Math.random() * 3) + 1), 1];
        var c = [Math.round((Math.random() * 40) - 15), 1]; 
        var d = [Math.round((Math.random() * 40) - 25), 1]; 
        
        const simple1 = simplify([a[0], c[0]]);
        const simple2 = simplify([b[0], d[0]]);
        a = [simple1[0], 1];
        c = [simple1[1], 1];
        b = [simple2[0], 1];
        d = [simple2[1], 1];

        quad_coef = fracProd(multiplier, fracProd(a, b)); 
        lin_coef = fracProd(multiplier, fracSum(fracProd(a, d), fracProd(b, c))); 
        const_coef = fracProd(multiplier, fracProd(c, d)); 

        var quad_term = `${clean(quad_coef, addsign=false)}x^2` 
        var lin_term; 
        if (lin_coef[0] == 0) {
            lin_term = ``;
        } else {lin_term = `${clean(lin_coef, addsign=true)}x`;}
        var const_term = `${clean(const_coef, addsign=true)}`

        if (a[0] == b[0] && c[0] == d[0]) {
            return [`Factor: $ ${quad_term} ${lin_term} ${const_term}$`, `$${clean(multiplier, addsign=false)} (${clean(a, addsign=false)} x ${clean(c, addsign=true)})^2$`]
        } else {
            return [`Factor: $ ${quad_term} ${lin_term} ${const_term}$`, `$${clean(multiplier, addsign=false)} (${clean(a, addsign=false)} x ${clean(c, addsign=true)})(${clean(b, addsign=false)} x ${clean(d, addsign=true)})$`]
        }
    }
}

function QuadS_V(level) {
    // Generating a quadratic equation to convert from standard to vertex
    if (level == 1) {
        var lin_coef = [2 * Math.round((Math.random() * 12) - 6), 1]; 
        var const_coef = [Math.round((Math.random() * 40) - 20), 1]; 
        var h = [(lin_coef[0])/2, 1];
        var k = [const_coef[0] - h[0]**2, 1];
        var lin_term; 
        if (lin_coef[0] == 0) {
            lin_term = ``;
        } else {lin_term = `${clean(lin_coef, addsign=true)}x`;}
        return [`Complete the square: $x^2 ${lin_term} ${clean(const_coef, addsign=true)}$`, `$(x ${clean(h, addsign=true)})^2 ${clean(k, addsign=true)}$`]
    } else if (level == 2) {
        var quad_coef = [Math.round((Math.random() * 6) - 3), 1]; 
        var lin_coef = [2 * Math.round((Math.random() * 12) - 6), 1]; 
        var const_coef = [Math.round((Math.random() * 40) - 20), 1]; 
        while (quad_coef[0] == 0) {quad_coef = [Math.round((Math.random() * 4) - 2), 1]; }
        while (lin_coef[0] == 0) {lin_coef = [Math.round((Math.random() * 12) - 6), 1]; }

        var h = simplify([lin_coef[0], 2*quad_coef[0]]);
        var k = simplify(fracSum([-(lin_coef[0]**2), 4 * quad_coef[0]], const_coef));

        return [`Complete the square: $${clean(quad_coef, addsign=false)}x^2 ${clean(lin_coef, addsign=true)}x ${clean(const_coef, addsign=true)}$`, `${clean(quad_coef, addsign=false)}$(x ${clean(h, addsign=true)})^2 ${clean(k, addsign=true)}$`]
    } else if (level == 3) {
        var quad_coef = [Math.round((Math.random() * 10) - 5), 1]; 
        var lin_coef = [2 * Math.round((Math.random() * 20) - 10), 1]; 
        var const_coef = [Math.round((Math.random() * 50) - 25), 1]; 
        while (quad_coef[0] == 0) {quad_coef = [Math.round((Math.random() * 4) - 2), 1]; }
        while (lin_coef[0] == 0) {lin_coef = [Math.round((Math.random() * 12) - 6), 1]; }

        var h = simplify([lin_coef[0], 2*quad_coef[0]]);
        var k = simplify(fracSum([-(lin_coef[0]**2), 4 * quad_coef[0]], const_coef));

        return [`Complete the square: $${clean(quad_coef, addsign=false)}x^2 ${clean(lin_coef, addsign=true)}x ${clean(const_coef, addsign=true)}$`, `$${clean(quad_coef, addsign=false)}(x ${clean(h, addsign=true)})^2 ${clean(k, addsign=true)}$`]
    }
}

function QuadF_S(level) {
    // Generating a quadratic equation to convert from factored to standard
    if (level==1) {
        const alpha = [Math.round((Math.random() * 30) - 15), 1]; 
        const beta = [Math.round((Math.random() * 30) - 15), 1];

        var lin_coef = fracSum(alpha, beta); 
        var const_coef = fracProd(alpha, beta); 

        var lin_term;
        var const_term = `${clean(const_coef)}`;
        if (lin_coef[0] == 0) {lin_term = ``;}
        else if (lin_coef[0] == 1) {lin_term = `+x`;}
        else if (lin_coef[0] == -1) {lin_term = `-x`;}
        else {lin_term = `${clean(lin_coef)}x`;}

        return [`Expand the following: $(x ${clean(alpha)})(x ${clean(beta)})$`, `$x^2 ${lin_term} ${const_term}$`];
    } else if (level == 2) {
        var multiplier = [Math.round((Math.random() * 4) -2), 1];
        while (multiplier[0] == 0) {
            multiplier = [Math.round((Math.random() * 4) -2), 1];
        }
        var a = [Math.round((Math.random() * 6) - 3), 1]; 
        var b = [Math.round((Math.random() * 4) - 2), 1]; 
        var c = [Math.round((Math.random() * 30) - 15), 1]; 
        var d = [Math.round((Math.random() * 30) - 15), 1];

        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];} 
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2), 1];} 
        
        var quad_coef = fracProd(multiplier, fracProd(a, b)); 
        var lin_coef = fracProd(multiplier, fracSum(fracProd(a, d), fracProd(b, c))); 
        var const_coef = fracProd(multiplier, fracProd(c, d)); 

        var quad_term; 
        if (quad_coef[0] == 1) {quad_term = `x^2`;}
        else if (quad_coef[0] == -1) {quad_term = `-x^2`;}
        else {quad_term = `${clean(quad_coef, addsign=false)}x^2`;}

        var lin_term ;
        if (lin_coef[0] == 0) {lin_term = ``;}
        else if (lin_coef[0] == 1) {lin_term = `x`;}
        else if (lin_coef[0] == -1) {lin_term = `-x`;}
        else {lin_term = `${clean(lin_coef)}x`;}


        var const_term = `${clean(const_coef, addsign=true)}`;
        return [`Expand the following: $${clean(multiplier, addsign=false)}(${clean(a, addsign=false)}x ${clean(c)})(${clean(b, addsign=false)}x ${clean(d)})$`, `$${quad_term} ${lin_term} ${const_term}$`];
    } else if (level == 3) {
        var multiplier = [Math.round((Math.random() * 8) -4), 1];
        while (multiplier[0] == 0) {
            multiplier = [Math.round((Math.random() * 10) -5), 1];
        }
        var a = [Math.round((Math.random() * 10) - 5), 1]; 
        var b = [Math.round((Math.random() * 8) - 4), 1]; 
        var c = [Math.round((Math.random() * 40) - 20), 1]; 
        var d = [Math.round((Math.random() * 30) - 15), 1];

        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];} 
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2), 1];} 

        var quad_coef = fracProd(multiplier, fracProd(a, b)); 
        var lin_coef = fracProd(multiplier, fracSum(fracProd(a, d), fracProd(b, c))); 
        var const_coef = fracProd(multiplier, fracProd(c, d));

        var quad_term; 
        if (quad_coef[0] == 1) {quad_term = `x^2`;}
        else if (quad_coef[0] == -1) {quad_term = `-x^2`;}
        else {quad_term = `${clean(quad_coef, addsign=false)}x^2`;}
        
        var lin_term 
        if (lin_coef[0] == 0) {lin_term = ``;}
        else if (lin_coef[0] == 1) {lin_term = `x`;}
        else if (lin_coef[0] == -1) {lin_term = `-x`;}
        else {lin_term = `${clean(lin_coef)}x`;}

        var const_term = `${clean(const_coef, addsign=true)}`;
        return [`Expand the following: $${clean(multiplier, addsign=false)}(${clean(a, addsign=false)}x ${clean(c)})(${clean(b, addsign=false)}x ${clean(d)})$`, `$${quad_term} ${lin_term} ${const_term}$`];
    }
}

function QuadV_S(level) {
    // Generating a quadratic equation to convert from vertex to standard
    if (level == 1) {
        var a = [1, 1]; 
        var h = randNumGen(1); 
        var k = randNumGen(1); 
    } else if (level == 2) {
        var a = [Math.round((Math.random() * 6) - 3), 1]; 
        var h = [Math.round((Math.random() * 10) - 5), 1]; 
        var k = randNumGen(2); 
    } else if (level == 3) {
        var a = randNumGen(2); 
        var h = randNumGen(2); 
        var k = randNumGen(3); 
    }
    var quad_coef = a;
    var lin_coef = fracProd([2, 1], fracProd(a, h));
    var const_coef = fracSum(fracProd(a, fracProd(h, h)), k);

    var lin_term; 
    if (lin_coef[0] == 0) {lin_term = ``;}
    else {lin_term = `${clean(lin_coef)}x`;}
    var const_term = clean(const_coef);
    
    return [`Expand the following: $${clean(quad_coef, addsign=false)}(x ${clean(h)})^2 ${clean(k)}$`, `$${clean(quad_coef, addsign=false)}x^2 ${lin_term} ${const_term}$`];
    
}

function QuadF_V(level) {
    if (level == 1) {
        var m = [1, 1]; 
        var a = [1, 1];
        var b = [1, 1]; 
        var c = randNumGen(1); 
        var d = randNumGen(1); 
        while ((c[0] + d[0])%2 != 0) {d = randNumGen(1);}
        
    } else if (level == 2) {
        var m = [Math.round((Math.random() * 4) - 2), 1]; 
        var a = [Math.round((Math.random() * 3)), 1];
        var b = [1, 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 3)), 1];}
        var c = [Math.round((Math.random() * 10) - 5), 1]; 
        var d = [Math.round((Math.random() * 10) - 5), 1]; 
    } else if (level == 3) {
        var m = [Math.round((Math.random() * 8) - 4), 1]; 
        var a = [Math.round((Math.random() * 6) - 3), 1];
        var b = [Math.round((Math.random() * 4) - 2), 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 8) - 4), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2), 1];}
        var c = [Math.round((Math.random() * 20) - 10), 1]; 
        var d = [Math.round((Math.random() * 18) - 9), 1]; 
    }

    var quad_coef = fracProd(m, fracProd(a, b));
    var num = fracSum(fracProd(a, d), fracProd(b, c));
    var den = fracProd([2, 1], fracProd(a, b));
    h = fracProd(num, [den[1], den[0]]); 
    k = fracSum(fracProd(fracProd(fracProd(h, h), fracProd(a, b)), [-m[0], m[1]]), fracProd(m, fracProd(c, d))); 
    
    return [`Convert to Vertex Form: $${clean(quad_coef, addsign=false)}(${clean(a, addsign=false)}x ${clean(c)}) (${clean(b, addsign=false)}x ${clean(d)})$`, `$${clean(quad_coef, addsign=false)}(x ${clean(h)})^2 ${clean(k)}$`];
}

function QuadV_F(level) {
    if (level == 1) {
        var m = [1, 1]; 
        var a = [1, 1];
        var b = [1, 1]; 
        var c = randNumGen(1); 
        var d = randNumGen(1); 
    } else if (level == 2) {
        var m = [Math.round((Math.random() * 4) - 2), 1]; 
        var a = [Math.round((Math.random() * 3)), 1];
        var b = [1, 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 3)), 1];}
        var c = [Math.round((Math.random() * 10) - 5), 1]; 
        var d = [Math.round((Math.random() * 10) - 5), 1]; 
    } else if (level == 3) {
        var m = [Math.round((Math.random() * 8) - 4), 1]; 
        var a = [Math.round((Math.random() * 6) - 3), 1];
        var b = [Math.round((Math.random() * 4) - 2), 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 8) - 4), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2), 1];}
        var c = [Math.round((Math.random() * 20) - 10), 1]; 
        var d = [Math.round((Math.random() * 18) - 9), 1]; 
    }
    var quad_coef = fracProd(m, fracProd(a, b));
    var lin_coef = fracProd(m, fracSum(fracProd(a, d), fracProd(b, c))); 
    var const_coef = fracProd(m, fracProd(c, d)); 

    h = fracProd(fracProd(lin_coef, [quad_coef[1], quad_coef[0]]), [1, 2]); 
    k = fracSum(fracProd(fracProd(fracProd(h, h), quad_coef), [-1, 1]), const_coef); 
    
    
    return [`Convert to Factored Form: $${clean(quad_coef, addsign=false)}(x ${clean(h)})^2 ${clean(k)}$`, `$${clean(quad_coef, addsign=false)}(${clean(a, addsign=false)}x ${clean(c)}) (${clean(b, addsign=false)}x ${clean(d)})$`];
}

function CubicS_F(level) {
    if (level == 1) {
        var m = [1, 1]; 
        var a = [1, 1];
        var b = [1, 1]; 
        var c = [1, 1]; 
        var d = randNumGen(1); 
        var e = randNumGen(1); 
        var f = randNumGen(1); 
    } else if (level == 2) {
        var m = [Math.round((Math.random() * 4) - 2), 1];
        var a = [Math.round((Math.random() * 4) - 2), 1];
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 4) - 2), 1];}
        var b = [1, 1]; 
        var c = [1, 1]; 
        var d = [Math.round((Math.random() * 20) - 10), 1]; 
        var e = [Math.round((Math.random() * 20) - 10), 1];
        var f = randNumGen(1); 
    } else if (level == 3) {
        var m = [Math.round((Math.random() * 6) - 3), 1];
        var a = [Math.round((Math.random() * 4) - 2), 1];
        var b = [Math.round((Math.random() * 6) - 3), 1]; 
        var c = [1, 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 6) - 3), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 4) - 2), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 6) - 3), 1];}
        var d = [Math.round((Math.random() * 20) - 10), 1]; 
        var e = [Math.round((Math.random() * 20) - 10), 1];
        var f = [Math.round((Math.random() * 24) - 12), 1];
    }
    const simple1 = simplify([a[0], d[0]]);
    const simple2 = simplify([b[0], e[0]]);
    const simple3 = simplify([c[0], f[0]]);
    a = [simple1[0], 1];
    d = [simple1[1], 1];
    b = [simple2[0], 1];
    e = [simple2[1], 1];
    c = [simple3[0], 1];
    f = [simple3[1], 1];

    var cub_coef = fracProd(fracProd(m, c), fracProd(a, b)); 
    var quad_coef = fracProd(m, fracSum(fracProd(b, fracSum(fracProd(c, d), fracProd(a, f))), fracProd(a, fracProd(c,e)))); 
    var lin_coef = fracProd(m, fracSum(fracProd(d, fracSum(fracProd(c, e), fracProd(b, f))), fracProd(a, fracProd(e, f)))); 
    var const_coef = fracProd(fracProd(m, d), fracProd(e, f)); 

    var cub_term, quad_term, lin_term, const_term; 
    cub_term = `${clean(cub_coef, addsign=false)} x^3`; 
    if (quad_coef[0] == 0) {quad_term = ``;} 
    else if (quad_coef[0] == quad_coef[1]) {quad_term = `+ x^2`;}
    else if (quad_coef[0] == -quad_coef[1]) {quad_term = `- x^2`;}
    else {quad_term = `${clean(quad_coef)} x^2`;}
    if (lin_coef[0] == 0) {lin_term = ``;} 
    else if (lin_coef[0] == lin_coef[1]) {lin_term = " + x";}
    else if (lin_coef[0] == -lin_coef[1]) {lin_term = " - x";}
    else {lin_term = `${clean(lin_coef)}x`}
    const_term = clean(const_coef); 

    var solution; 
    
    console.log(`${a[0]} ${b[0]} ${c[0]} ${d[0]} ${e[0]} ${f[0]}`);
    console.log(allEqual([a[0], b[0], c[0]]) && allEqual([d[0], e[0], f[0]]))
    
    if (allEqual([a[0], b[0], c[0]]) && allEqual([d[0], e[0], f[0]])) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)})^3$`} 
    else if (a[0] == b[0] && d[0] == e[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)})^2 (${clean(c, addsign=false)}x ${clean(f)})$`}
    else if (a[0] == c[0] && d[0] == f[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)})^2 (${clean(b, addsign=false)}x ${clean(e)})$`}
    else if (b[0] == c[0] && e[0] == f[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)}) (${clean(c, addsign=false)}x ${clean(f)})^2$`}
    else {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)})(${clean(b, addsign=false)}x ${clean(e)})(${clean(c, addsign=false)}x ${clean(f)})$`}

    return [`Factor: $${cub_term} ${quad_term} ${lin_term} ${const_term}$`, solution]
}

function CubicF_S(level) {
    if (level == 1) {
        var m = [1, 1]; 
        var a = [1, 1];
        var b = [1, 1]; 
        var c = [1, 1]; 
        var d = randNumGen(1); 
        var e = randNumGen(1); 
        var f = randNumGen(1); 
    } else if (level == 2) {
        var m = [Math.round((Math.random() * 4) - 2), 1]; 
        var a = [Math.round((Math.random() * 6) - 3), 1];
        var b = [Math.round((Math.random() * 4) - 2)+1, 1]; 
        var c = [Math.round((Math.random() * 4) - 2)+2, 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2)+1, 1]; }
        while (c[0] == 0) {c = [Math.round((Math.random() * 4) - 2)+2, 1]; }
        var d = [Math.round((Math.random() * 20) - 10), 1]; 
        var e = [Math.round((Math.random() * 20) - 10), 1]; 
        var f = [Math.round((Math.random() * 20) - 10), 1];
    } else if (level == 3) {
        var m = [Math.round((Math.random() * 8) - 4), 1]; 
        var a = randNumGen(2);
        var b = randNumGen(2); 
        var c = randNumGen(2); 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = randNumGen(2);}
        while (b[0] == 0) {b = randNumGen(2); }
        while (c[0] == 0) {c = randNumGen(2); }
        var d = randNumGen(3); 
        var e = randNumGen(2); 
        var f = randNumGen(2);
    }

    var cub_coef = fracProd(fracProd(m, c), fracProd(a, b)); 
    var quad_coef = fracProd(m, fracSum(fracProd(b, fracSum(fracProd(c, d), fracProd(a, f))), fracProd(a, fracProd(c,e)))); 
    var lin_coef = fracProd(m, fracSum(fracProd(d, fracSum(fracProd(c, e), fracProd(b, f))), fracProd(a, fracProd(e, f)))); 
    var const_coef = fracProd(fracProd(m, d), fracProd(e, f)); 

    var cub_term, quad_term, lin_term, const_term; 
    cub_term = `${clean(cub_coef, addsign=false)} x^3`; 
    if (quad_coef[0] == 0) {quad_term = ``;} 
    else if (quad_coef[0] == quad_coef[1]) {quad_term = `+ x^2`;}
    else if (quad_coef[0] == -quad_coef[1]) {quad_term = `- x^2`;}
    else {quad_term = `${clean(quad_coef)} x^2`;}
    if (lin_coef[0] == 0) {lin_term = ``;} 
    else if (lin_coef[0] == lin_coef[1]) {lin_term = " + x";}
    else if (lin_coef[0] == -lin_coef[1]) {lin_term = " - x";}
    else {lin_term = `${clean(lin_coef)}x`}
    const_term = clean(const_coef); 
    return [`Expand: $${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)})(${clean(b, addsign=false)}x ${clean(e)})(${clean(c, addsign=false)}x ${clean(f)})$`, `$${cub_term} ${quad_term} ${lin_term} ${const_term}$`]
}

function QuarticS_F(level) {
    if (level == 1) {
        var m = [1, 1]; 
        var a = [1, 1];
        var b = [1, 1]; 
        var c = [1, 1]; 
        var d = [1, 1]; 
        var e = randNumGen(1); 
        var f = randNumGen(1); 
        var g = randNumGen(1); 
        var h = randNumGen(1); 
    } else if (level == 2) {
        var m = [Math.round((Math.random() * 4) - 2), 1]; 
        var a = [Math.round((Math.random() * 6) - 3), 1];
        var b = [Math.round((Math.random() * 4) - 2), 1]; 
        var c = [Math.round((Math.random() * 4) - 2), 1]; 
        var d = [1,1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2), 1]; }
        while (c[0] == 0) {c = [Math.round((Math.random() * 4) - 2), 1]; }
        while (d[0] == 0) {d = [1, 1]; }
        var e = [Math.round((Math.random() * 20) - 10), 1]; 
        var f = [Math.round((Math.random() * 20) - 10), 1]; 
        var g = [Math.round((Math.random() * 20) - 10), 1];
        var h = [Math.round((Math.random() * 20) - 10), 1];

    } else if (level == 3) {
        var m = [Math.round((Math.random() * 8) - 4), 1]; 
        var a = [Math.round((Math.random() * 8) - 4), 1];
        var b = [Math.round((Math.random() * 6) - 3), 1]; 
        var c = [Math.round((Math.random() * 4) - 2), 1]; 
        var d = [Math.round((Math.random() * 4) - 2), 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 8) - 4), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 6) - 3), 1]; }
        while (c[0] == 0) {c = [Math.round((Math.random() * 4) - 2), 1]; }
        while (d[0] == 0) {d = [Math.round((Math.random() * 4) - 2), 1]; }
        var e = [Math.round((Math.random() * 20) - 10), 1]; 
        var f = [Math.round((Math.random() * 20) - 10), 1];
        var g = [Math.round((Math.random() * 16) - 8), 1]; 
        var h = [Math.round((Math.random() * 16) - 8), 1];
    }

    const simple1 = simplify([a[0], e[0]])
    const simple2 = simplify([b[0], f[0]])
    const simple3 = simplify([c[0], g[0]])
    const simple4 = simplify([d[0], h[0]])

    a = [simple1[0], 1];
    e = [simple1[1], 1];
    b = [simple2[0], 1];
    f = [simple2[1], 1];
    c = [simple3[0], 1]; 
    g = [simple3[1], 1];
    d = [simple4[0], 1];
    h = [simple4[1], 1];

    var quar_coef = fracProd(m, fracProd(fracProd(a, b), fracProd(c, d))); 
    var cub_coef = fracProd(m, fracSum(fracProd(fracProd(a, b), fracSum(fracProd(c, h), fracProd(g, d))), fracProd(fracProd(c, d), fracSum(fracProd(a, f), fracProd(e, b))))); 
    var quad_coef = fracProd(m, fracSum(fracProd(fracSum(fracProd(a, h), fracProd(d, e)), fracSum(fracProd(b, g), fracProd(c, f))), fracSum(fracProd(fracProd(a, d), fracProd(f, g)), fracProd(fracProd(b, c), fracProd(e, h))))); 
    var lin_coef = fracProd(m, fracSum(fracProd(fracProd(g, h), fracSum(fracProd(a, f), fracProd(b, e))), fracProd(fracProd(e, f), fracSum(fracProd(c, h), fracProd(d, g))))); 
    var const_coef = fracProd(m, fracProd(fracProd(e, f), fracProd(g, h))); 

    var quar_term, cub_term, quad_term, lin_term, const_term; 
    quar_term = `${clean(quar_coef, addsign=false)} x^4`;
    
    if (cub_coef[0] == 0) {cub_term = ``;} 
    else if (cub_coef[0] == cub_coef[1]) {cub_term = `+ x^3`;}
    else if (cub_coef[0] == -cub_coef[1]) {cub_term = `- x^3`;}
    else {cub_term = `${clean(cub_coef)} x^3`;}

    if (quad_coef[0] == 0) {quad_term = ``;} 
    else if (quad_coef[0] == quad_coef[1]) {quad_term = `+ x^2`;}
    else if (quad_coef[0] == -quad_coef[1]) {quad_term = `- x^2`;}
    else {quad_term = `${clean(quad_coef)} x^2`;}

    if (lin_coef[0] == 0) {lin_term = ``;} 
    else if (lin_coef[0] == lin_coef[1]) {lin_term = " + x";}
    else if (lin_coef[0] == -lin_coef[1]) {lin_term = " - x";}
    else {lin_term = `${clean(lin_coef)}x`}
    const_term = clean(const_coef);
    
    var solution; 

    console.log(`${a[0]} ${b[0]} ${c[0]} ${d[0]} ${e[0]} ${f[0]} ${g[0]} ${h[0]}`);

    if (allEqual([a[0], b[0], c[0], d[0]]) && allEqual([e[0], f[0], g[0], h[0]])) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(d)})^3$`} 
    else if (allEqual([a[0], b[0], c[0]]) && allEqual([e[0], f[0], g[0]])) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^3 (${clean(d, addsign=false)}x ${clean(h)})$`}
    else if (allEqual([a[0], b[0], d[0]]) && allEqual([e[0], f[0], h[0]])) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^3 (${clean(c, addsign=false)}x ${clean(g)})$`}
    else if (allEqual([a[0], c[0], d[0]]) && allEqual([e[0], g[0], h[0]])) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^3 (${clean(b, addsign=false)}x ${clean(f)})$`}
    else if (allEqual([b[0], c[0], d[0]]) && allEqual([f[0], g[0], h[0]])) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})(${clean(b, addsign=false)}x ${clean(f)})^3 $`}

    else if (a[0] == b[0] && e[0] == f[0] && c[0] == d[0] && g[0] == h[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^2 (${clean(c, addsign=false)}x ${clean(g)})^2$`}
    else if (a[0] == c[0] && e[0] == g[0] && b[0] == d[0] && f[0] == h[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^2 (${clean(b, addsign=false)}x ${clean(f)})^2$`}
    else if (a[0] == d[0] && e[0] == h[0] && b[0] == c[0] && f[0] == g[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^2 (${clean(b, addsign=false)}x ${clean(f)})^2$`}

    else if (a[0] == b[0] && e[0] == f[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^2 (${clean(c, addsign=false)}x ${clean(g)})(${clean(d, addsign=false)}x ${clean(h)})$`}
    else if (a[0] == c[0] && e[0] == g[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^2 (${clean(b, addsign=false)}x ${clean(f)})(${clean(d, addsign=false)}x ${clean(h)})$`}
    else if (a[0] == d[0] && e[0] == h[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})^2 (${clean(b, addsign=false)}x ${clean(f)})(${clean(c, addsign=false)}x ${clean(g)})$`}
    else if (b[0] == c[0] && f[0] == g[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})(${clean(b, addsign=false)}x ${clean(f)})^2 (${clean(d, addsign=false)}x ${clean(h)})$`}
    else if (b[0] == d[0] && f[0] == h[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})(${clean(b, addsign=false)}x ${clean(f)})^2 (${clean(c, addsign=false)}x ${clean(g)})$`}
    else if (c[0] == d[0] && g[0] == h[0]) {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})(${clean(b, addsign=false)}x ${clean(f)})(${clean(c, addsign=false)}x ${clean(g)})^2$`}

    else {solution = `$${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})(${clean(b, addsign=false)}x ${clean(f)})(${clean(c, addsign=false)}x ${clean(g)})(${clean(d, addsign=false)}x ${clean(h)})$`}

    return [`Factor: $${quar_term} ${cub_term} ${quad_term} ${lin_term} ${const_term}$`, solution]
}

function QuarticF_S(level) {
    if (level == 1) {
        var m = [1, 1]; 
        var a = [1, 1];
        var b = [1, 1]; 
        var c = [1, 1]; 
        var d = [1, 1]; 
        var e = randNumGen(1); 
        var f = randNumGen(1); 
        var g = randNumGen(1); 
        var h = randNumGen(1); 
    } else if (level == 2) {
        var m = [Math.round((Math.random() * 4) - 2), 1]; 
        var a = [Math.round((Math.random() * 6) - 3), 1];
        var b = [Math.round((Math.random() * 4) - 2)+1, 1]; 
        var c = [Math.round((Math.random() * 4) - 2)+2, 1]; 
        var d = [1,1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = [Math.round((Math.random() * 6) - 3), 1];}
        while (b[0] == 0) {b = [Math.round((Math.random() * 4) - 2)+1, 1]; }
        while (c[0] == 0) {c = [Math.round((Math.random() * 4) - 2)+2, 1]; }
        while (d[0] == 0) {d = [1, 1]; }
        var e = [Math.round((Math.random() * 20) - 10), 1]; 
        var f = [Math.round((Math.random() * 20) - 10), 1]; 
        var g = [Math.round((Math.random() * 20) - 10), 1];
        var h = [Math.round((Math.random() * 20) - 10), 1];
    } else if (level == 3) {
        var m = [Math.round((Math.random() * 8) - 4), 1]; 
        var a = randNumGen(2);
        var b = randNumGen(2); 
        var c = randNumGen(2); 
        var d = [Math.round((Math.random() * 4) - 2)+2, 1]; 
        while (m[0] == 0) {m = [Math.round((Math.random() * 4) - 2), 1];}
        while (a[0] == 0) {a = randNumGen(2);}
        while (b[0] == 0) {b = randNumGen(2); }
        while (c[0] == 0) {c = randNumGen(2); }
        while (d[0] == 0) {d = [Math.round((Math.random() * 4) - 2)+2, 1]; }
        var e = randNumGen(3); 
        var f = [Math.round((Math.random() * 20) - 10), 1];
        var g = randNumGen(2); 
        var h = [Math.round((Math.random() * 20) - 10), 1];
    }

    var quar_coef = fracProd(m, fracProd(fracProd(a, b), fracProd(c, d))); 
    var cub_coef = fracProd(m, fracSum(fracProd(fracProd(a, b), fracSum(fracProd(c, h), fracProd(g, d))), fracProd(fracProd(c, d), fracSum(fracProd(a, f), fracProd(e, b))))); 
    var quad_coef = fracProd(m, fracSum(fracProd(fracSum(fracProd(a, h), fracProd(d, e)), fracSum(fracProd(b, g), fracProd(c, f))), fracSum(fracProd(fracProd(a, d), fracProd(f, g)), fracProd(fracProd(b, c), fracProd(e, h))))); 
    var lin_coef = fracProd(m, fracSum(fracProd(fracProd(g, h), fracSum(fracProd(a, f), fracProd(b, e))), fracProd(fracProd(e, f), fracSum(fracProd(c, h), fracProd(d, g))))); 
    var const_coef = fracProd(m, fracProd(fracProd(e, f), fracProd(g, h))); 

    var quar_term, cub_term, quad_term, lin_term, const_term; 
    quar_term = `${clean(quar_coef, addsign=false)} x^4`;
    
    if (cub_coef[0] == 0) {cub_term = ``;} 
    else if (cub_coef[0] == cub_coef[1]) {cub_term = `+ x^3`;}
    else if (cub_coef[0] == -cub_coef[1]) {cub_term = `- x^3`;}
    else {cub_term = `${clean(cub_coef)} x^3`;}

    if (quad_coef[0] == 0) {quad_term = ``;} 
    else if (quad_coef[0] == quad_coef[1]) {quad_term = `+ x^2`;}
    else if (quad_coef[0] == -quad_coef[1]) {quad_term = `- x^2`;}
    else {quad_term = `${clean(quad_coef)} x^2`;}

    if (lin_coef[0] == 0) {lin_term = ``;} 
    else if (lin_coef[0] == lin_coef[1]) {lin_term = " + x";}
    else if (lin_coef[0] == -lin_coef[1]) {lin_term = " - x";}
    else {lin_term = `${clean(lin_coef)}x`}
    const_term = clean(const_coef); 
    return [`Expand: $${clean(m, addsign=false)}(${clean(a, addsign=false)}x ${clean(e)})(${clean(b, addsign=false)}x ${clean(f)})(${clean(c, addsign=false)}x ${clean(g)})(${clean(d, addsign=false)}x ${clean(h)})$`, `$${quar_term} ${cub_term} ${quad_term} ${lin_term} ${const_term}$`]
}

function PolyF_S(level) {
    const cubic_or_quartic = Math.round((Math.random()));
    if (cubic_or_quartic == 0) {return CubicF_S(level);}
    else {return QuarticF_S(level);}
}

function PolyS_F(level) {
    const cubic_or_quartic = Math.round(Math.random()); 
    if (cubic_or_quartic == 0) {return CubicS_F(level);} 
    else {return QuarticS_F(level); }
}

var func_dict = {
    "Linear: Slope-Intercept to Point-Slope" : LinSI_PS, 
    "Linear: Point-Slope to Slope-Intercept" : LinPS_SI, 
    "Quadratic: Standard to Factored" : QuadS_F, 
    "Quadratic: Standard to Vertex" : QuadS_V, 
    "Quadratic: Factored to Standard" : QuadF_S, 
    "Quadratic: Factored to Vertex" : QuadF_V, 
    "Quadratic: Vertex to Standard" : QuadV_S, 
    "Quadratic: Vertex to Factored" : QuadV_F, 
    "Polynomial: Factored to Standard": PolyF_S, 
    "Polynomial: Standard to Factored": PolyS_F
}

var section_no = 0;
function GenerateConvertExercises(no_Q) { 
    section_no += 1;
    var level = document.getElementById("Dropdown_Level0").value;
    var func_name = func_dict[document.getElementById("Dropdown_Convert0").value];
    const polynomial_section = document.getElementById("Polynomials");
    var section = document.createElement('div'); 
    section.style = "border: solid 1px; margin-bottom: 2%;"; 
    polynomial_section.appendChild(section); 
    
    var section_headerPoly = document.createElement('div'); 
    section_headerPoly.style = "border-bottom: solid 1px black; display: flex; height: 30px;"; 
    section.appendChild(section_headerPoly); 

    var title = document.createElement('h3'); 
    title.innerHTML = `${document.getElementById("Dropdown_Convert0").value} [Lvl.${level}]`;
    title.style = "border: solid 0px green; width: 57%; margin: 4px 10px;" 

    var title_solutions = document.createElement('h3');
    title_solutions.innerHTML = `Solutions`; 
    title_solutions.style = "margin: 4px 25px;"; 

    var solution_button = document.createElement('button'); 
    solution_button.innerHTML = `Section ${section_no} Solutions`; 
    solution_button.classList.add("Solution_Button"); 
    solution_button.style = "width: 20%; height: 24px; margin: 3px 0px; display: none; position: absolute; right: 20px; "; 
    
    section_headerPoly.appendChild(title); 
    section_headerPoly.appendChild(title_solutions); 
    section_headerPoly.appendChild(solution_button);

    solution_button.onclick = function() {
        var number = solution_button.innerHTML[8];
        var solutions = document.getElementsByClassName(`section${number}solutions`);
        for (let i = 0; i < solutions.length; i++) {
            solutions[i].style = "position: absolute; left: 80%; display: inline-block;"; 
        }
    };
    list = document.createElement('ol'); 
    list.style = "margin-left: 0px; padding: 0px 20px; "
    for (let i = 1; i <= no_Q ; i++) {
        line = document.createElement('li');
        line.style = "margin: 3px 0px; border: solid 1px grey; width: 99%; padding:1px; height: 25px; position: relative; "; 
        ex_sol = func_name(level);
        list.appendChild(line);

        var exercise = document.createElement('span'); 
        exercise.style = "float: left; width: 55%;"; 
        exercise.innerHTML = `${ex_sol[0]}`;
        line.appendChild(exercise); 

        var input_log = document.createElement('input'); 
        input_log.style = "width: 120px; height: 18px; margin-top: 1px; position: absolute; left: 60%;";
        input_log.setAttribute("id", `Input${section_no}.${i}`);
        line.appendChild(input_log); 

        

        var reply_click = function() {
            const number = this.id.slice(6);
            var input_information = document.getElementById(`Input${number}`).value.replace(/ /g,'');
            
            document.getElementById(`Input${number}`).disabled = true; 
            var actual_solution = document.getElementById(`Solution${number}`).value.replace(/ /g,''); 
            var indices = []; 
            for (let i = 0; i < actual_solution.length; i++) {
                if (actual_solution[i] === "\{" || actual_solution[i] === "\}") {indices.push(i)};
            }
            var decimals = []; 
            var frac_start_end = []; 
            while (indices.length != 0) {
                const first = indices[0]; 
                const second = indices[1]; 
                const third = indices[2]; 
                const fourth = indices[3]; 
                frac_start_end.push(first-5);
                frac_start_end.push(fourth); 
                numerator = actual_solution.substring(first + 1, second);
                denominator = actual_solution.substring(third + 1, fourth);
                decimals.push((numerator/denominator).toFixed(1));
                indices = indices.slice(4); 
            }
            
            while (frac_start_end.length != 0) {
                first_part = actual_solution.substring(0, frac_start_end[frac_start_end.length - 2]);
                second_part = decimals[decimals.length - 1]; 
                third_part = actual_solution.substring(frac_start_end[frac_start_end.length - 1] + 1); 
                // alert(`One ${first_part}`); 
                // alert(`Two ${second_part}`);
                // alert(`Three ${third_part}`); 
                actual_solution =  first_part + second_part + third_part; 
                frac_start_end = frac_start_end.slice(0, -2); 
                decimals = decimals.slice(0, -1); 
            }
            const function_name = document.getElementById("Dropdown_Convert0").value; 

            if (function_name != 'Quadratic: Factored to Standard' && function_name != 'Quadratic: Vertex to Standard' && function_name != 'Polynomial: Factored to Standard') {
                input_information = input_information.replace(/x\^2/g, '(x)^2');
                input_information = input_information.replace(/x\^3/g, '(x)^3');
                input_information = input_information.replace(/x\^4/g, '(x)^4');
                input_information = input_information.replace(/\)x\(/g, ')(x)(');
            }

            if (function_name == "Quadratic: Standard to Factored" || function_name == "Quadratic: Vertex to Factored" || function_name == "Polynomial: Standard to Factored") {
                var actual_solution_factors = actual_solution.split(')').join(',').split('(').join(',').split(',');
                actual_solution = actual_solution_factors.filter(function (el) {
                    return el != '';
                }).sort().join(' '); 

                var input_information_factors = input_information.split(')').join(',').split('(').join(',').split(',');
                input_information = input_information_factors.filter(function (el) {
                    return el != '';
                }).sort().join(' '); 

                console.log(actual_solution); 
                console.log(input_information);
            }

            if (function_name)

            if (input_information == actual_solution) {
                
                document.getElementById(`Solution${number}`).style = "position: absolute; left: 80%; display: auto; color: rgb(11, 225, 0);"; 
            } 
            else {

                document.getElementById(`Solution${number}`).style = "position: absolute; left: 80%; display: auto; color: red;"; 
            }
        }


        var submit_button = document.createElement('button'); 
        submit_button.innerHTML = `Submit`; 
        submit_button.setAttribute("id",`Button${section_no}.${i}`);
        submit_button.onclick = reply_click; 
        submit_button.style = "width: 50px; height: 24px; margin-top: 1px; padding: 1px 1px; display: auto; position: absolute; left: 69%; "; 
        line.appendChild(submit_button); 

        //input_log.addEventListener("keyup", function(event) {
        //    if (event.code == "Enter") {
        //        event.preventDefault(); 
        //        reply_click; }
        //})

        var solution = document.createElement('span'); 
        solution.style = "position: absolute; left: 55%; display: none; color: blue;"; 
        solution.setAttribute("class", `section${section_no}solutions`);
        solution.setAttribute("id", `Solution${section_no}.${i}`)

        line.appendChild(solution); 
        solution.innerHTML = `${ex_sol[1]}`; 
        solution.value = `${ex_sol[1]}`.slice(1, -1); 

        MathJax.Hub.Queue(["Typeset", MathJax.Hub, line]);
        
    }
    section.appendChild(list); 
}

const box = document.getElementById("box")
console.log(box);

box.addEventListener("click", e => {
    console.log("Box")
}); 