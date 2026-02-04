/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_big.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 21:52:19 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 22:01:47 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

//this will assign indexes for the elements in the stack
static void	index_stack(t_stack *stack)
{
	//we are using indexes instead of raw integers to sort using radix sort, for example:
	//12 134 -12 -354 will be
	//0  1   2   3  in indexes, so it will handle positive and negative integers the same
}

void radix_sort(t_stack **a, t_stack **b)
{
	//implement the radix_sort algorithm
}