/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   metrics.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 22:04:07 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 20:34:32 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

double	compute_disorder(t_stack *a)
{
	long	mistake;
	long	total_pairs;
	t_stack	*i;
	t_stack	*j;

	if (!a || !a->next)
		return (0.0);
	i = a;
	mistake = 0;
	total_pairs = 0;
	while (i)
	{
		j = i->next;
		while (j)
		{
			total_pairs += 1;
			if (i->value > j->value)
				mistake += 1;
			j = j->next;
		}
		i = i->next;
	}
	if (total_pairs == 0)
		return (0.0);
	return ((double)mistake / (double)total_pairs);
}
