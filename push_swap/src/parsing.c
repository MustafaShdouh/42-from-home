/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:02:48 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 21:23:32 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void parse_args(int argv, char **argv, t_stack **stack_a)
{
	int	i;
	
	long	nb;
	i = 0;
	while (i < argc)
	{
		//call syntax check
		if (error_syntax(argv[i]))
			ft_error(stack_a);
		//later we need to consider a string input like "1 2 3" 4 --> we need to use ft_split to split it and treat it as more than two inputs
		nb = ft_atol(argv[i]);
		//do a limit check
		if (nb > INT_MAX || nb < INT_MIN)
			ft_error(stack_a);
		//call duplicate check
		if (error_duplicate(argv[i], nb))
			ft_error(stack_a);
		stack_add_back(stack_a, stack_new((int)nb));
		i++;
	}
}