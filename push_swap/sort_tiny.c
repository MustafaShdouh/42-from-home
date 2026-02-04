/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_tiny.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:59:50 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 21:52:11 by mel-shdo         ###   ########.fr       */
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

// this method is for stacks that have 4 or 5 inputs
void	sort_five(t_stack **a, t_stack **b)
{
	//made so that it can point at the smallest number
	t_stack *smallest;

	//while the stack is greater than 3, it cant be sorted with sort_three(), so we reduce the number of elements until theyre three
	while (stack_size(*a) > 3)
	{
		//we make smallest point to the smallest value
		smallest = find_min(*a);
		//while the top of the stack is not the smallest value we keep rotating until it is on top
		while (*a != smallest)
			ra(a);
		//we then put the smallest value in stack b
		pb(a, b);
	}
	//here we are guaranteed to have 3 values, so we just call sort_three()
	sort_three(a);
	//here we make sure the values in stack b (which are sorted from biggest to smallest) are pushed back into b (biggest pushed first)
	while (*b)
		pa(a, b);
}