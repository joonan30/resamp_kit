# Bernoulli trials are sequences of independent dichotomous trials, each with probability 0.5 of success.
swap_index <- rbinom(n=nFams, size=1, prob = 0.5)
nSwap = sum(swap_index==1)

# Create swapped and non-swapped samples
swapFams <- fams[swap_index==1]
noSwapFams <- fams[!fams %in% swapFams]
