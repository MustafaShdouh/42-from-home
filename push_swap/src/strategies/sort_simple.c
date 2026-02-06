/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 20:51:45 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 21:22:57 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

// this method is for stacks with only three inputs
void	sort_three(t_stack **a)
{
	t_stack	*big_node;

	//find where the biggest number is and point to it
	big_node = find_max(*a);
	//if it is at the top then execute ra and put it at the bottom
	if (*a == big_node)
		ra(a);
	//if it is in the middle then execute rra and put it at the bottom
	else if ((*a)->next == big_node)
		rra(a);
	//if it is at the bottom then do nothing (no code for this possibility)
	
	//if the first number is bigger than the second then execute sa and swap the numbers
	if ((*a)->content > (a*)->next->content)
		sa(a);
	//if the first number is smaller than the second then do nothing (no code for this possibility)
}

