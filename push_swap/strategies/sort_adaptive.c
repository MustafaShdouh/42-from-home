/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_adaptive.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 22:05:48 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 22:20:17 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_adaptive(t_stack **a, t_stack **b)
{
	float	disorder;

	disorder = compute_disorder(*a);
	if (disorder < 0.2f)
		sort_simple(a, b);
	else if (disorder < 0.5f)
		sort_medium(a, b);
	else
		sort_complex(a, b);
}