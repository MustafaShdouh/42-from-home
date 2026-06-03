/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:14:09 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/14 00:40:41 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void rotate_stack(t_stack **s)
{
	t_stack	*tail;
	t_stack	*head;

	if (!s || !*s || !(*s)->next)
		return ;
	head = *s;
	tail = stack_last(*s);
	*s = head->next;
	(*s)->prev = NULL;
	tail->next = head;
	head->prev = tail;
	head->next = NULL;
}

void	ra(t_stack **a)
{
	rotate_stack(a);
	get_stats()->ra++;
	if (get_stats()->print_ops)
	write(1, "ra\n", 3);
}

void	rb(t_stack **b)
{
	rotate_stack(b);
	get_stats()->rb++;
	if (get_stats()->print_ops)
	write(1, "rb\n", 3);
}

void	rr(t_stack **a, t_stack **b)
{
	rotate_stack(a);
	rotate_stack(b);
	get_stats()->rr++;
	if (get_stats()->print_ops)
	write(1, "rr\n", 3);
}